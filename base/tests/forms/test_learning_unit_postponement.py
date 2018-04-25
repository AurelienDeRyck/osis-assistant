##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from unittest import mock
import factory
import factory.fuzzy

from django.forms import model_to_dict
from django.http import QueryDict

from base.forms.learning_unit.learning_unit_create_2 import PartimForm, FullForm
from base.forms.learning_unit.learning_unit_postponement import LearningUnitPostponementForm
from base.forms.utils import acronym_field
from base.models import entity_container_year
from base.models.enums import entity_container_year_link_type
from base.models.learning_unit import LearningUnit
from base.models.learning_unit_year import LearningUnitYear
from base.tests.factories.business.learning_units import GenerateContainer, GenerateAcademicYear
from base.tests.factories.learning_unit import LearningUnitFactory

from django.test import TestCase

from base.forms.learning_unit.learning_unit_create import LearningUnitYearModelForm, \
    LearningUnitModelForm, EntityContainerFormset, LearningContainerYearModelForm, LearningContainerModelForm
from base.models.enums import learning_unit_year_subtypes
from base.tests.factories.academic_year import create_current_academic_year
from base.tests.factories.learning_unit_year import LearningUnitYearFactory
from base.tests.factories.person import PersonFactory
from base.tests.factories.person_entity import PersonEntityFactory

FULL_ACRONYM = 'LAGRO1000'
SUBDIVISION_ACRONYM = 'C'


class LearningUnitPostponementFormContextMixin(TestCase):
    """This mixin is used in this test file in order to setup an environment for testing LEARNING UNIT POSTPONEMENT
       FORM"""
    def setUp(self):
        self.current_academic_year = create_current_academic_year()
        self.generated_ac_years = GenerateAcademicYear(self.current_academic_year.year + 1,
                                                       self.current_academic_year.year + 10)

        # Creation of a LearingContainerYear and all related models - FOR 6 years
        self.learn_unit_structure = GenerateContainer(self.current_academic_year.year,
                                                      self.current_academic_year.year + 6)
        # Build in Generated Container [first index = start Generate Container ]
        self.generated_container_year = self.learn_unit_structure.generated_container_years[0]

        # Update All full learning unit year acronym
        LearningUnitYear.objects.filter(learning_unit=self.learn_unit_structure.learning_unit_full)\
                                .update(acronym=FULL_ACRONYM)
        # Update All partim learning unit year acronym
        LearningUnitYear.objects.filter(learning_unit=self.learn_unit_structure.learning_unit_partim) \
                                .update(acronym=FULL_ACRONYM + SUBDIVISION_ACRONYM)

        self.learning_unit_year_full = LearningUnitYear.objects.get(
            learning_unit=self.learn_unit_structure.learning_unit_full,
            academic_year=self.current_academic_year
        )

        self.person = PersonFactory()
        for entity in self.learn_unit_structure.entities:
            PersonEntityFactory(person=self.person, entity=entity)


# class TestLearningUnitPostponementFormInit(LearningUnitPostponementFormContextMixin):
#     """Unit tests for LearningUnitPostponementForm.__init__()"""
#     def test_wrong_instance_args(self):
#         wrong_instance = LearningUnitFactory()
#         with self.assertRaises(AttributeError):
#             _instanciate_postponement_form(instance=wrong_instance, person=self.person)
#
#     def test_consistency_property_default_value_is_true(self):
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#         self.assertTrue(form.check_consistency)
#
#     def test_forms_property_end_year_is_none(self):
#         self.learn_unit_structure.learning_unit_full.end_year = None
#         self.learn_unit_structure.learning_unit_full.save()
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#
#         self.assertIsInstance(form._forms_to_upsert, list)
#         self.assertIsInstance(form._forms_to_delete, list)
#         self.assertEqual(len(form._forms_to_upsert), 6)
#         self.assertFalse(form._forms_to_delete)
#
#     def test_forms_property_end_year_is_current_year(self):
#         self.learn_unit_structure.learning_unit_full.end_year = self.current_academic_year.year
#         self.learn_unit_structure.learning_unit_full.save()
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#
#         self.assertFalse(form._forms_to_upsert)
#         self.assertEqual(len(form._forms_to_delete), 6)
#
#     def test_forms_property_end_year_is_more_than_current_and_less_than_none(self):
#         self.learn_unit_structure.learning_unit_full.end_year = self.current_academic_year.year + 2
#         self.learn_unit_structure.learning_unit_full.save()
#
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#
#         self.assertEqual(len(form._forms_to_upsert), 2)
#         self.assertEqual(len(form._forms_to_delete), 4)
#
#     def test_forms_property_no_learning_unit_year_in_future(self):
#         self.learn_unit_structure.learning_unit_full.end_year = None
#         self.learn_unit_structure.learning_unit_full.save()
#         LearningUnitYear.objects.filter(
#             learning_unit=self.learn_unit_structure.learning_unit_full,
#             academic_year__year__gt=self.current_academic_year.year
#         ).delete()
#
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#
#         self.assertEqual(len(form._forms_to_upsert), 6)
#         self.assertFalse(form._forms_to_delete)
#
#
# class TestLearningUnitPostponementFormIsValid(LearningUnitPostponementFormContextMixin):
#     """Unit tests for LearningUnitPostponementForm.is_valid()"""
#     @mock.patch('base.forms.learning_unit_postponement.LearningUnitPostponementForm._check_consistency',
#                 side_effect=None)
#     def test_is_valid_with_consitency_property_to_false(self, mock_check_consistency):
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#         form.check_consistency = False
#         self.assertTrue(form.is_valid())
#         self.assertFalse(mock_check_consistency.called)
#
#     @mock.patch('base.forms.learning_unit_postponement.LearningUnitPostponementForm._check_consistency',
#                 side_effect=None)
#     def test_is_valid_with_consitency_property_to_true(self, mock_check_consistency):
#         instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
#         form = _instanciate_postponement_form(instance_luy_base_form, self.person)
#         form.check_consistency = False
#         mock_check_consistency.assert_called_once_with()


class TestLearningUnitPostponementFormSave(LearningUnitPostponementFormContextMixin):

    @mock.patch('base.forms.learning_unit.learning_unit_create_2.FullForm.save', side_effect=None)
    def test_save_with_all_luy_to_create(self, mock_baseform_save):
        """This test will ensure that the save will call LearningUnitBaseForm [CREATE] for all luy
           No update because all LUY doesn't exist on db
        """
        LearningUnitYear.objects.filter(
            learning_unit=self.learn_unit_structure.learning_unit_full,
            academic_year__year__gt=self.current_academic_year.year
        ).delete()
        instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
        form = _instanciate_postponement_form(instance_luy_base_form, self.person)
        self.assertEqual(len(form._forms_to_upsert), 6)

        form.save()
        self.assertEqual(mock_baseform_save.call_count, 6)

    @mock.patch('base.forms.learning_unit.learning_unit_create_2.FullForm.save', side_effect=None)
    def test_save_with_luy_to_upsert(self, mock_baseform_save):
        """This test will ensure that the save will call LearningUnitBaseForm [CREATE/UPDATE] for all luy
           2 Update because LUY exist until current_academic_year + 2
           4 Create because LUY doesn't exist after current_academic_year + 2
        """
        LearningUnitYear.objects.filter(
            learning_unit=self.learn_unit_structure.learning_unit_full,
            academic_year__year__gt= self.current_academic_year.year + 2
        ).delete()

        instance_luy_base_form = _instanciate_base_learning_unit_form(self.learning_unit_year_full, self.person)
        form = _instanciate_postponement_form(instance_luy_base_form, self.person)
        self.assertEqual(len(form._forms_to_upsert), 6)

        form.save()
        self.assertEqual(mock_baseform_save.call_count, 4)


def _instanciate_base_learning_unit_form(learning_unit_year_instance, person):
    entity_version_by_type = entity_container_year.find_last_entity_version_grouped_by_linktypes(
        learning_unit_year_instance.learning_container_year
    )
    form = FullForm if learning_unit_year_instance.subtype == learning_unit_year_subtypes.FULL else PartimForm
    form_args = {
        'learning_unit_year_full': learning_unit_year_instance.parent,
        'instance': learning_unit_year_instance,
        'data': {
            'acronym': learning_unit_year_instance.acronym,
            'acronym_0': learning_unit_year_instance.acronym[0],
            'acronym_1': learning_unit_year_instance.acronym[1:],
            'subtype': learning_unit_year_instance.subtype,
            'academic_year': learning_unit_year_instance.academic_year.id,
            'specific_title': learning_unit_year_instance.specific_title,
            'specific_title_english': learning_unit_year_instance.specific_title_english,
            'credits': learning_unit_year_instance.credits,
            'session': learning_unit_year_instance.session,
            'quadrimester': learning_unit_year_instance.quadrimester,
            'status': learning_unit_year_instance.status,
            'internship_subtype': learning_unit_year_instance.internship_subtype,
            'attribution_procedure': learning_unit_year_instance.attribution_procedure,

            # Learning unit data model form
            'periodicity': learning_unit_year_instance.learning_unit.periodicity,
            'faculty_remark': learning_unit_year_instance.learning_unit.faculty_remark,
            'other_remark': learning_unit_year_instance.learning_unit.other_remark,

            # Learning container year data model form
            'campus': learning_unit_year_instance.learning_container_year.campus.id,
            'language': learning_unit_year_instance.learning_container_year.language.id,
            'common_title': learning_unit_year_instance.learning_container_year.common_title,
            'common_title_english': learning_unit_year_instance.learning_container_year.common_title_english,
            'container_type': learning_unit_year_instance.learning_container_year.container_type,
            'type_declaration_vacant': learning_unit_year_instance.learning_container_year.type_declaration_vacant,
            'team': learning_unit_year_instance.learning_container_year.team,
            'is_vacant': learning_unit_year_instance.learning_container_year.is_vacant,

            'entitycontaineryear_set-0-entity':
                entity_version_by_type.get(entity_container_year_link_type.REQUIREMENT_ENTITY).id,
            'entitycontaineryear_set-1-entity':
                entity_version_by_type.get(entity_container_year_link_type.ALLOCATION_ENTITY).id,
            'entitycontaineryear_set-2-entity':
                entity_version_by_type.get(entity_container_year_link_type.ADDITIONAL_REQUIREMENT_ENTITY_1).id,
            'entitycontaineryear_set-3-entity':
                entity_version_by_type.get(entity_container_year_link_type.ADDITIONAL_REQUIREMENT_ENTITY_2).id,
            'entitycontaineryear_set-INITIAL_FORMS': '0',
            'entitycontaineryear_set-MAX_NUM_FORMS': '4',
            'entitycontaineryear_set-MIN_NUM_FORMS': '4',
            'entitycontaineryear_set-TOTAL_FORMS': '4',
        },
        'person': person
    }
    return form(**form_args)


def _instanciate_postponement_form(instance, person):
    return LearningUnitPostponementForm(instance, person)