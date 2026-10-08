"""Experiment 008 curriculum correctness and bounded training checks."""
import json
from collections import Counter

import pytest
import torch

from prototypes.rnn_llm_architecture import experiment_008 as ex


def test_curriculum_schedule_and_fixed_controls():
    cfg=ex.Config(steps_per_stage=3)
    a=ex.make_schedule("curriculum",3,seed=17)
    b=ex.make_schedule("shuffled",3,seed=17)
    assert a==(16,)*3+(32,)*3+(64,)*3+(128,)*3
    assert Counter(a)==Counter(b)=={16:3,32:3,64:3,128:3}
    assert b==ex.make_schedule("shuffled",3,seed=17)
    assert ex.make_schedule("fixed64",3,seed=17)==(64,)*12
    assert ex.make_schedule("fixed128",3,seed=17)==(128,)*12
    assert len(ex.make_schedule("curriculum",cfg.steps_per_stage,seed=17))==12


def test_same_examples_across_matching_length_occurrences():
    from prototypes.rnn_llm_architecture.experiment_004 import _paired_inputs
    for d in (16,32,64,128):
        for idx in (0,3):
            s=ex.sample_seed(17,d,idx)
            a,y,_=_paired_inputs(d,6,seed=s)
            b,z,_=_paired_inputs(d,6,seed=s)
            assert torch.equal(a,b) and torch.equal(y,z)
            assert ex.sample_seed(17,d,idx)!=ex.sample_seed(17,d,idx+1)


def test_bad_config_and_schedule():
    for kwargs in ({"variants":("bad",)},{"seeds":(-1,)},{"schedules":("no",)},
                   {"steps_per_stage":0},{"batch_size":0},{"learning_rate":float("nan")},
                   {"max_wall_seconds":0}):
        with pytest.raises(ValueError):ex.Config(**kwargs)
    for args in (("bogus",1,17),("shuffled",0,17),("shuffled",1,-1)):
        with pytest.raises(ValueError):ex.make_schedule(args[0],args[1],seed=args[2])


def test_short_native_training_and_no_overwrite(tmp_path):
    cfg=ex.Config(variants=("protected_w32",),seeds=(17,),schedules=("curriculum",),
                  steps_per_stage=1,batch_size=2,eval_examples=16,max_wall_seconds=120)
    out=tmp_path/"exp008.json"
    r=ex.execute(cfg,output=out)
    assert r["status"]=="complete" and not r["skipped"]
    assert len(r["runs"])==1
    row=r["runs"][0]
    assert row["length_counts"]=={"16":1,"32":1,"64":1,"128":1}
    assert row["steps_completed"]==4
    assert row["training_examples"]==8
    assert row["approx_training_tokens"]==2*(16+32+64+128)
    for d in (16,64,128,256):
        assert row["evaluation"][str(d)]["paired_on_unequal"] is not None
    assert json.loads(out.read_text())["runs"][0]["complete"]
    with pytest.raises(FileExistsError):ex.execute(cfg,output=out)


def test_global_budget_marks_skips(tmp_path,monkeypatch):
    monkeypatch.setattr(ex,"train_condition",lambda *args,**kwargs:{"complete":False,"steps_completed":0,"evaluation":{}})
    c=ex.Config(variants=("gru_w32",),seeds=(17,),schedules=("curriculum","fixed64"),
                steps_per_stage=1,max_wall_seconds=30)
    out=tmp_path/"expired.json"
    r=ex.execute(c,output=out)
    assert r["status"]=="budget_limited" and len(r["skipped"])==1
