# -*- coding: utf-8 -*-


def question_save(sender, instance, created, **kwargs):
    instance.generate()
