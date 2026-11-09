# -*- coding: utf-8 -*-
"""Eventos do pygame que podem nao existir em versoes antigas."""
import pygame

FOCUS_LOST = getattr(pygame, "WINDOWFOCUSLOST", None)
TEXT_INPUT = getattr(pygame, "TEXTINPUT", None)
