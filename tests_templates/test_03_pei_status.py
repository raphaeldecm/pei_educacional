"""
Testes de Status do PEI (Plano Educacional Individualizado)
============================================================

Funcionalidade: Atualização automática de status do PEI

Regra de Negócio:
O PEI possui 5 campos obrigatórios que devem ser preenchidos:
1. adapted_objective
2. adapted_content
3. adapted_methodology
4. adapted_resources
5. adapted_assessments

O status é atualizado AUTOMATICAMENTE ao salvar, baseado em quantos
campos foram preenchidos:

- NOT_START: 0 campos preenchidos
- IN_PROGRESS: 1 a 4 campos preenchidos
- FEEDBACK: Todos os 5 campos preenchidos
- COMPLETED: Status manual (não muda mais automaticamente)

Critérios a Aplicar:
1. Classes de Equivalência (CE): Quantidade de campos preenchidos
2. Análise de Valor Limite (VL): Transições entre status (0→1, 4→5 campos)

Orientações:
- Identifique as partições baseadas na quantidade de campos
- Teste as transições de status
- Teste que COMPLETED não muda automaticamente
- Documente cada teste
"""

import pytest

from sistema_pei.academics.tests.factories import EnrollmentFactory
from sistema_pei.people.tests.factories import TeacherFactory

pytestmark = pytest.mark.django_db


# ============================================================================
# PLANEJAMENTO DETALHADO
# ============================================================================
#
# ANÁLISE DA FUNCIONALIDADE: update_status()
# -------------------------------------------
#
# ENTRADA: Quantidade de campos preenchidos (0 a 5)
# SAÍDA: Status do PEI
#
# Classes de Equivalência:
# | ID  | Descrição              | Campos | Status Esperado | Válida? |
# |-----|------------------------|--------|-----------------|---------|
# | CE1 | Nenhum campo           | 0      | NOT_START       | Válida  |
# | CE2 | Início (1 campo)       | 1      | IN_PROGRESS     | Válida  |
# | CE3 | Meio (2-3 campos)      | 2-3    | IN_PROGRESS     | Válida  |
# | CE4 | Quase completo         | 4      | IN_PROGRESS     | Válida  |
# | CE5 | Todos os campos        | 5      | FEEDBACK        | Válida  |
# | CE6 | Status manual          | N/A    | COMPLETED       | Válida  |
#
# Valores Limite:
# | Limite                      | Valores de Teste           |
# |-----------------------------|----------------------------|
# | Transição 0→1 campos        | 0, 1                       |
# | Transição 4→5 campos        | 4, 5                       |
#
# Casos de Teste Necessários:
# 1. test_status_not_started_zero_fields (VL, CE1)
# 2. test_status_in_progress_one_field (VL, CE2)
# 3. test_status_in_progress_two_fields (CE, CE3)
# 4. test_status_in_progress_three_fields (CE, CE3)
# 5. test_status_in_progress_four_fields (VL, CE4)
# 6. test_status_feedback_all_fields (VL, CE5)
# 7. test_status_completed_does_not_change (CE, CE6)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture()
def enrollment():
    """Matrícula válida para criar PEIs."""
    return EnrollmentFactory()


@pytest.fixture()
def teacher():
    """Professor responsável pelo PEI."""
    return TeacherFactory()


# ============================================================================
# TESTES: Atualização Automática de Status
# ============================================================================


class TestPeiStatusUpdate:
    """Testes para atualização automática de status do PEI."""

    def test_status_not_started_zero_fields(self, enrollment, teacher):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE1 (0 campos)
        Resultado Esperado: status == NOT_START
        """
        # IMPLEMENTE
        # Dica: Pei.objects.create() com todos os campos vazios ("")
        #       pei.refresh_from_db() para recarregar

    def test_status_in_progress_one_field(self, enrollment, teacher):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (1 campo - limite mínimo para IN_PROGRESS)
        Resultado Esperado: status == IN_PROGRESS
        """
        # IMPLEMENTE
        # Dica: Preencha apenas 1 campo (ex: adapted_objective)
        #       Deixe os outros 4 vazios

    def test_status_in_progress_two_fields(self, enrollment, teacher):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (2 campos - meio da partição)
        Resultado Esperado: status == IN_PROGRESS
        """
        # IMPLEMENTE: PEI com 2 campos preenchidos

    def test_status_in_progress_three_fields(self, enrollment, teacher):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (3 campos - meio da partição)
        Resultado Esperado: status == IN_PROGRESS
        """
        # IMPLEMENTE: PEI com 3 campos preenchidos

    def test_status_in_progress_four_fields(self, enrollment, teacher):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE4 (4 campos - limite máximo para IN_PROGRESS)
        Resultado Esperado: status == IN_PROGRESS
        """
        # IMPLEMENTE: PEI com 4 campos preenchidos

    def test_status_feedback_all_five_fields(self, enrollment, teacher):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE5 (5 campos - todos preenchidos)
        Resultado Esperado: status == FEEDBACK
        """
        # IMPLEMENTE
        # Dica: Preencha todos os 5 campos obrigatórios

    def test_status_completed_does_not_change_on_update(
        self,
        enrollment,
        teacher,
    ):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE6 (Status COMPLETED não deve mudar)
        Resultado Esperado: status permanece COMPLETED
        """
        # IMPLEMENTE
        # 1. Criar PEI com todos os campos
        # 2. Marcar status como COMPLETED manualmente
        # 3. Editar um campo (limpar)
        # 4. Verificar que status ainda é COMPLETED

    def test_status_updates_automatically_on_save(self, enrollment, teacher):
        """
        Critério: Classes de Equivalência (CE)
        Objetivo: Verificar que status atualiza AUTOMATICAMENTE ao salvar
        Cenário: Criar PEI vazio, adicionar campos gradualmente, verificar status
        """
        # IMPLEMENTE: Teste incremental
        # 1. Criar PEI vazio → verificar NOT_START
        # 2. Adicionar 1 campo e save() → verificar IN_PROGRESS
        # 3. Completar todos os campos e save() → verificar FEEDBACK


# ============================================================================
# TESTES ADICIONAIS: Métodos Auxiliares
# ============================================================================


class TestPeiMissingOpinions:
    """
    Testes para o método get_missing_opinions().

    Este método retorna lista de pareceres que ainda não foram preenchidos.
    """

    def test_get_missing_opinions_all_missing(self, enrollment, teacher):
        """
        Cenário: PEI sem nenhum parecer preenchido
        Resultado: Lista com todos os pareceres faltando
        """
        # IMPLEMENTE
        # PEI sem pareceres deve retornar lista com:
        # ["1º Bimestre", "2º Bimestre", "3º Bimestre", "4º Bimestre", "Parecer Final"]
        # (considere se é disciplina anual ou semestral)

    def test_get_missing_opinions_some_filled(self, enrollment, teacher):
        """
        Cenário: PEI com alguns pareceres preenchidos
        Resultado: Lista apenas com os faltantes
        """
        # IMPLEMENTE

    def test_get_missing_opinions_all_filled(self, enrollment, teacher):
        """
        Cenário: PEI com todos os pareceres preenchidos
        Resultado: Lista vazia
        """
        # IMPLEMENTE

    def test_has_missing_opinions(self, enrollment, teacher):
        """
        Teste o método has_missing_opinions()
        """
        # IMPLEMENTE


# ============================================================================
# ORIENTAÇÕES FINAIS
# ============================================================================

# CHECKLIST:
# □ Implementei testes para todos os valores de status:
#   □ NOT_START (0 campos)
#   □ IN_PROGRESS (1, 2, 3, 4 campos)
#   □ FEEDBACK (5 campos)
#   □ COMPLETED (não muda)
# □ Testei valores limite (0→1, 4→5)
# □ Testei valores do meio das partições (2, 3)
# □ Testei que COMPLETED não muda
# □ Testei métodos auxiliares (get_missing_opinions, has_missing_opinions)
# □ Documentei cada teste
# □ Todos os testes passam: pytest tests_templates/test_03_pei_status.py -v
#
# DICAS:
# - Crie PEI com Pei.objects.create()
# - Use pei.refresh_from_db() para recarregar do banco após save()
# - Campos vazios devem ser "" (string vazia), não None
# - Para disciplinas semestrais, apenas 2 bimestres + final são necessários
# - Execute: pytest tests_templates/test_03_pei_status.py -v -k "status"
#
# COMANDOS ÚTEIS:
# # Rodar todos os testes
# pytest tests_templates/ -v
#
# # Rodar apenas testes de status
# pytest tests_templates/test_03_pei_status.py::TestPeiStatusUpdate -v
#
# # Ver qual teste específico está falhando
# pytest tests_templates/test_03_pei_status.py::TestPeiStatusUpdate::test_status_not_started_zero_fields -v -s  # noqa: E501
