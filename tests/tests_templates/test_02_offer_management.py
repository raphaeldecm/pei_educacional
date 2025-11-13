"""
Testes de Gestão de Ofertas (Offer Management)
===============================================

Funcionalidades:
1. Adicionar aluno em oferta (offer.add_student)
2. Remover aluno de oferta (offer.remove_student)

Regras de Negócio:
- Adicionar: Apenas em ofertas ABERTAS, aluno não pode estar duplicado
- Remover: Remove matrícula e deleta PEIs associados automaticamente

Critérios a Aplicar:
1. Classes de Equivalência (CE): Status da oferta, aluno duplicado/novo
2. Análise de Valor Limite (VL): Transições de estado

Orientações:
- Identifique as partições para cada funcionalidade
- Teste cenários válidos e inválidos
- Verifique efeitos colaterais (deleção em cascata)
- Documente cada teste
"""

import pytest

from sistema_pei.academics.models import Offer
from sistema_pei.academics.tests.factories import CourseFactory
from sistema_pei.academics.tests.factories import OfferFactory
from sistema_pei.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture()
def user():
    """Usuário para usar nos testes."""
    return UserFactory()


@pytest.fixture()
def course():
    """Curso válido para testes."""
    return CourseFactory()


@pytest.fixture()
def open_offer(course):
    """Oferta aberta para testes."""
    return OfferFactory(
        status=Offer.OfferStatus.OPEN,
        course=course,
    )


@pytest.fixture()
def closed_offer(course):
    """Oferta fechada para testes."""
    return OfferFactory(
        status=Offer.OfferStatus.CLOSED,
        course=course,
    )


# ============================================================================
# PLANEJAMENTO SUGERIDO
# ============================================================================
#
# FUNCIONALIDADE: Adicionar Aluno (add_student)
# ----------------------------------------------
# Classes de Equivalência:
# - CE1: Oferta ABERTA + aluno novo (Válida)
# - CE2: Oferta FECHADA (Inválida)
# - CE3: Oferta ABERTA + aluno já matriculado (Inválida)
#
# Casos de Teste Necessários:
# 1. test_add_student_to_open_offer_success
# 2. test_add_student_to_closed_offer_fails
# 3. test_add_duplicate_student_fails
# 4. test_add_student_creates_enrollment_with_correct_data
#
# FUNCIONALIDADE: Remover Aluno (remove_student)
# -----------------------------------------------
# Classes de Equivalência:
# - CE1: Aluno matriculado na oferta (Válida)
# - CE2: Aluno NÃO matriculado na oferta (Inválida)
# - CE3: Aluno com PEI associado (Válida - deve deletar PEI)
#
# Casos de Teste Necessários:
# 1. test_remove_student_success
# 2. test_remove_nonexistent_student_fails
# 3. test_remove_student_deletes_associated_pei


# ============================================================================
# TESTES: Adicionar Aluno em Oferta
# ============================================================================


class TestOfferAddStudent:
    """
    Testes para adicionar aluno em oferta (offer.add_student).

    Regra: Apenas ofertas ABERTAS aceitam novos alunos.
    Aluno não pode estar duplicado na mesma oferta.

    IMPLEMENTE OS TESTES SEGUINDO O EXEMPLO DO test_00_exemplo_completo.py:
    - Identifique as partições (CE)
    - Teste cenários válidos e inválidos
    - Verifique dados da matrícula criada
    - Documente cada teste
    """

    def test_add_student_to_open_offer_success(self, open_offer, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE1 (Válida - oferta aberta, aluno novo)
        Resultado Esperado: Matrícula criada
        """
        # IMPLEMENTE
        # Dica: student = StudentFactory(course=open_offer.course)
        #       enrollment = open_offer.add_student(student, user)

    def test_add_student_to_closed_offer_fails(self, closed_offer, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE2 (Inválida - oferta fechada)
        Resultado Esperado: ValidationError
        """
        # IMPLEMENTE
        # Dica: Use pytest.raises(ValidationError)

    def test_add_duplicate_student_fails(self, open_offer, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (Inválida - aluno já matriculado)
        Resultado Esperado: ValidationError
        """
        # IMPLEMENTE
        # Dica: Adicione o aluno uma vez, depois tente adicionar novamente

    def test_add_student_creates_enrollment_with_correct_data(
        self,
        open_offer,
        user,
    ):
        """
        Critério: Classes de Equivalência (CE)
        Cenário: Verificar dados da matrícula criada
        Resultado Esperado: created_by, updated_by corretos
        """
        # IMPLEMENTE
        # Verifique: enrollment.created_by == user
        #            enrollment.updated_by == user


# ============================================================================
# TESTES: Remover Aluno de Oferta
# ============================================================================


class TestOfferRemoveStudent:
    """Testes para remover aluno de oferta."""

    def test_remove_student_success(self, open_offer, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE1 (Válida - aluno matriculado)
        Resultado Esperado: Matrícula deletada
        """
        # IMPLEMENTE
        # 1. Adicionar estudante na oferta
        # 2. Guardar enrollment_id
        # 3. Remover estudante
        # 4. Verificar que enrollment não existe mais

    def test_remove_nonexistent_student_fails(self, open_offer):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE2 (Inválida - aluno não matriculado)
        Resultado Esperado: ValidationError
        """
        # IMPLEMENTE
        # Dica: Crie estudante mas NÃO adicione na oferta

    def test_remove_student_deletes_associated_pei(self, open_offer, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (aluno com PEI)
        Resultado Esperado: Remove enrollment E deleta PEI associado

        IMPORTANTE: Este teste verifica deleção em cascata!
        """
        # IMPLEMENTE ESTE TESTE IMPORTANTE
        # 1. Criar e adicionar estudante
        # 2. Criar um PEI para essa matrícula (você precisará de PeiFactory)
        # 3. Verificar que PEI e Enrollment existem
        # 4. Remover estudante
        # 5. Verificar que matrícula NÃO existe mais
        # 6. Verificar que PEI NÃO existe mais


# ============================================================================
# TESTES ADICIONAIS (Opcional)
# ============================================================================


class TestOfferStudentManagementEdgeCases:
    """Casos extremos e cenários adicionais (opcional)."""

    def test_available_students_excludes_enrolled_students(self, open_offer):
        """
        Teste: available_students() retorna apenas alunos não matriculados
        """
        # IMPLEMENTE (opcional)

    def test_student_count_updates_correctly(self, open_offer, user):
        """
        Teste: student_count() atualiza ao adicionar/remover
        """
        # IMPLEMENTE (opcional)


# ============================================================================
# ORIENTAÇÕES FINAIS
# ============================================================================

# CHECKLIST:
# □ Implementei testes para adicionar aluno (4 testes)
# □ Implementei testes para remover aluno (3 testes)
# □ Testei cenários válidos E inválidos
# □ Testei deleção em cascata (PEI)
# □ Documentei cada teste
# □ Todos passam: pytest tests_templates/test_02_offer_management.py -v
#
# DICAS IMPORTANTES:
# - Para criar PEI: from sistema_pei.educational_plan.models import Pei
#   pei = Pei.objects.create(enrollment=enrollment, ...)
# - Use Pei.objects.filter(id=pei_id).exists() para verificar existência
# - Deleção em cascata é importante - PEI depende de Enrollment
# - Execute: pytest tests_templates/test_02_offer_management.py -v
#
# COMANDOS ÚTEIS:
# # Rodar apenas testes de adicionar
# pytest tests_templates/test_02_offer_management.py::TestOfferAddStudent -v
#
# # Rodar apenas testes de remover
# pytest tests_templates/test_02_offer_management.py::TestOfferRemoveStudent -v
#
# # Ver exemplo completo
# pytest tests_templates/test_00_exemplo_completo.py::TestOfferAddStudent -v
