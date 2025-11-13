"""
Testes de Validação de Matrícula (Enrollment)
==============================================

Funcionalidade: Validar campos de matrícula (notas e faltas)

Regras de Negócio:
- grade (notas): Valores entre 0 e 100 (decimal)
- absences (faltas): Valores >= 0 (inteiro positivo)

Critérios a Aplicar:
1. Classes de Equivalência (CE): Agrupe valores em partições válidas/inválidas
2. Análise de Valor Limite (VL): Teste valores nos limites (antes, no, depois)

Orientações:
- Para cada campo, identifique as partições
- Teste pelo menos um valor de cada partição
- Teste os valores limite de cada partição
- Documente cada teste explicando critério, partição e resultado esperado
"""

import pytest

pytestmark = pytest.mark.django_db


# ============================================================================
# PLANEJAMENTO SUGERIDO
# ============================================================================
#
# CAMPO: grade (Notas - 0 a 100)
# -------------------------------
# Classes de Equivalência:
# - CE1: Valores < 0 (Inválida)
# - CE2: Valores entre 0 e 100 (Válida)
# - CE3: Valores > 100 (Inválida)
#
# Valores Limite:
# - Limite mínimo: -0.01, 0, 0.01
# - Limite máximo: 99.99, 100, 100.01
#
# CAMPO: absences (Faltas - >= 0)
# --------------------------------
# Classes de Equivalência:
# - CE1: Valores < 0 (Inválida)
# - CE2: Valor = 0 (Válida)
# - CE3: Valores > 0 (Válida)
#
# Valores Limite:
# - Limite mínimo: -1, 0, 1


# ============================================================================
# TESTES: Validação de Faltas (absences)
# ============================================================================


class TestEnrollmentAbsencesValidation:
    """
    Testes para validação do campo absences (faltas).

    IMPLEMENTE OS TESTES SEGUINDO O PADRÃO ACIMA:
    - Identifique as partições (CE)
    - Identifique os valores limite (VL)
    - Teste cenários válidos e inválidos
    - Documente cada teste
    """

    def test_absences_valid_zero(self):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (Válida - zero)
        Valor: 0 (limite mínimo)
        Resultado Esperado: Faltas aceitas
        """
        # IMPLEMENTE

    def test_absences_valid_one(self):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE3 (Válida - positivo)
        Valor: 1 (logo acima do mínimo)
        Resultado Esperado: Faltas aceitas
        """
        # IMPLEMENTE

    def test_absences_valid_positive_value(self):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (Válida)
        Valor: 10 (valor positivo)
        Resultado Esperado: Faltas aceitas
        """
        # IMPLEMENTE

    def test_absences_invalid_negative(self):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE1 (Inválida - negativo)
        Valor: -1 (logo abaixo do mínimo)
        Resultado Esperado: ValidationError
        """
        # IMPLEMENTE: Use pytest.raises(ValidationError)

    def test_absences_invalid_negative_value(self):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE1 (Inválida)
        Valor: -10 (valor negativo)
        Resultado Esperado: ValidationError
        """
        # IMPLEMENTE


# ============================================================================
# ORIENTAÇÕES FINAIS
# ============================================================================

# EXPLICAÇÃO: O que é full_clean()?
# ==================================
#
# full_clean() é um método do Django que executa TODAS as validações do modelo:
#
# 1. **Validação de Campos Individuais:**
#    - Verifica tipos de dados (int, decimal, string, etc.)
#    - Verifica tamanho máximo (max_length)
#    - Executa validators customizados (MinValueValidator, MaxValueValidator)
#    - Verifica campos obrigatórios (blank=False, null=False)
#
# 2. **Validação de Constraints:**
#    - unique_together (combinação única de campos)
#    - check constraints (regras SQL)
#    - Validações no método clean() do modelo
#
# 3. **Como Usar em Testes:**
#    enrollment = EnrollmentFactory.build(grade1=150)  # Criar sem salvar
#    enrollment.full_clean()  # Lança ValidationError se inválido
#    enrollment.save()  # Só salva se passou na validação
#
# 4. **Testando Exceções:**
#    with pytest.raises(ValidationError):
#        enrollment.full_clean()  # Espera que lance erro
#
# Por que usar full_clean() em testes?
# - save() NÃO executa validações automaticamente
# - full_clean() garante que todas as regras sejam verificadas
# - Testa validações como elas funcionarão na aplicação real
#
# CHECKLIST:
# □ Implementei 8-9 testes para grade (notas)
# □ Implementei 5 testes para absences (faltas)
# □ Testei valores limite (VL): -0.01, 0, 0.01, 99.99, 100, 100.01
# □ Testei valores de cada partição (CE)
# □ Testei cenários válidos E inválidos
# □ Usei full_clean() antes de save()
# □ Usei pytest.raises(ValidationError) para testes inválidos
# □ Documentei cada teste
# □ Todos passam: pytest tests_templates/test_01_enrollment_validation.py -v
#
# COMANDOS ÚTEIS:
# # Rodar todos os testes deste arquivo
# pytest tests_templates/test_01_enrollment_validation.py -v
#
# # Rodar apenas testes de grade
# pytest tests_templates/test_01_enrollment_validation.py::TestEnrollmentGradeValidation -v  # noqa: E501
#
# # Rodar teste específico
# pytest tests_templates/test_01_enrollment_validation.py::TestEnrollmentGradeValidation::test_grade_valid_at_minimum_boundary -v  # noqa: E501
#
# # Ver output detalhado (prints)
# pytest tests_templates/test_01_enrollment_validation.py -v -s
#
# # Comparar com exemplo completo
# pytest tests_templates/test_00_exemplo_completo.py::TestEnrollmentGradeValidation -v
