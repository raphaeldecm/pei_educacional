"""
TESTE EXEMPLO COMPLETO - REFERÊNCIA
====================================

Este arquivo serve como REFERÊNCIA para você entender como:
1. Estruturar testes funcionais com pytest
2. Aplicar o critério de Classes de Equivalência
3. Aplicar o critério de Análise de Valor Limite
4. Usar fixtures e factories
5. Testar exceções e validações

ESTUDE ESTE ARQUIVO antes de implementar os outros!
"""

from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from sistema_pei.academics.models import Enrollment
from sistema_pei.academics.models import Offer
from sistema_pei.academics.tests.factories import CourseFactory
from sistema_pei.academics.tests.factories import EnrollmentFactory
from sistema_pei.academics.tests.factories import OfferFactory
from sistema_pei.people.tests.factories import StudentFactory
from sistema_pei.users.tests.factories import UserFactory

# Marca todos os testes deste módulo para usar o banco de dados
pytestmark = pytest.mark.django_db


# ============================================================================
# FIXTURES - Dados reutilizáveis nos testes
# ============================================================================


@pytest.fixture()
def user():
    """Cria um usuário para usar nos testes."""
    return UserFactory()


@pytest.fixture()
def curso_valido():
    """Cria um curso válido para usar nos testes."""
    return CourseFactory(
        name="Análise e Desenvolvimento de Sistemas",
        period="NIGHT",
        duration_type="SEMESTER",
        number_of_periods=6,
    )


@pytest.fixture()
def oferta_aberta(curso_valido):
    """Cria uma oferta ABERTA para testes."""
    return OfferFactory(
        status=Offer.OfferStatus.OPEN,
        course=curso_valido,
        year=2025,
        semester=2,
    )


@pytest.fixture()
def oferta_fechada(curso_valido):
    """Cria uma oferta FECHADA para testes."""
    return OfferFactory(
        status=Offer.OfferStatus.CLOSED,
        course=curso_valido,
        year=2024,
        semester=1,
    )


# ============================================================================
# CLASSE DE TESTES: Validação de Notas (Enrollment.grade)
# ============================================================================


class TestEnrollmentGradeValidation:
    """
    Testa a validação do campo 'grade' (nota) da matrícula.

    REGRA DE NEGÓCIO: Notas devem estar entre 0 e 100

    CLASSES DE EQUIVALÊNCIA:
    - CE1 (Inválida): grade < 0
    - CE2 (Válida):   0 <= grade <= 100
    - CE3 (Inválida): grade > 100

    VALORES LIMITE:
    - Limite inferior: -0.01, 0, 0.01
    - Limite superior: 99.99, 100, 100.01
    """

    def test_grade_valid_at_minimum_boundary(self, user):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (Válida)
        Valor: 0 (limite mínimo válido)
        Resultado Esperado: Aceita a nota
        """
        # Arrange (Preparar)
        enrollment = EnrollmentFactory.create(
            grade1=Decimal("0"),
            created_by=user,
            updated_by=user,
        )

        # Act (Agir)
        enrollment.full_clean()  # Valida o modelo

        # Assert (Verificar)
        assert enrollment.grade1 == Decimal("0")
        assert Enrollment.objects.filter(id=enrollment.id).exists()

    def test_grade_valid_at_maximum_boundary(self, user):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (Válida)
        Valor: 100 (limite máximo válido)
        Resultado Esperado: Aceita a nota
        """
        # Arrange
        enrollment = EnrollmentFactory.create(
            grade1=Decimal("100"),
            created_by=user,
            updated_by=user,
        )

        # Act
        enrollment.full_clean()

        # Assert
        assert enrollment.grade1 == Decimal("100")

    def test_grade_valid_just_above_minimum(self, user):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (Válida)
        Valor: 0.01 (logo acima do limite mínimo)
        Resultado Esperado: Aceita a nota
        """
        # Arrange
        enrollment = EnrollmentFactory.create(
            grade2=Decimal("0.01"),
            created_by=user,
            updated_by=user,
        )

        # Act
        enrollment.full_clean()

        # Assert
        assert enrollment.grade2 == Decimal("0.01")

    def test_grade_valid_just_below_maximum(self, user):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE2 (Válida)
        Valor: 99.99 (logo abaixo do limite máximo)
        Resultado Esperado: Aceita a nota
        """
        # Arrange
        enrollment = EnrollmentFactory.create(
            grade3=Decimal("99.99"),
            created_by=user,
            updated_by=user,
        )

        # Act
        enrollment.full_clean()

        # Assert
        assert enrollment.grade3 == Decimal("99.99")

    def test_grade_valid_middle_value(self, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE2 (Válida)
        Valor: 50 (valor no meio da partição válida)
        Resultado Esperado: Aceita a nota
        """
        # Arrange
        enrollment = EnrollmentFactory.create(
            grade4=Decimal("50"),
            created_by=user,
            updated_by=user,
        )

        # Act
        enrollment.full_clean()

        # Assert
        assert enrollment.grade4 == Decimal("50")

    def test_grade_invalid_below_minimum(self, user, oferta_aberta):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE1 (Inválida)
        Valor: -0.01 (logo abaixo do limite mínimo)
        Resultado Esperado: Rejeita com ValidationError
        """
        # Arrange
        student = StudentFactory()
        enrollment = Enrollment(
            offer=oferta_aberta,
            student=student,
            grade1=Decimal("-0.01"),
            YearSemesterReference=1,
            created_by=user,
            updated_by=user,
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            enrollment.full_clean()

        # Verifica se o erro é realmente do campo grade1
        assert "grade1" in exc_info.value.message_dict

    def test_grade_invalid_above_maximum(self, user, oferta_aberta):
        """
        Critério: Análise de Valor Limite (VL)
        Partição: CE3 (Inválida)
        Valor: 100.01 (logo acima do limite máximo)
        Resultado Esperado: Rejeita com ValidationError
        """
        # Arrange
        student = StudentFactory()
        enrollment = Enrollment(
            offer=oferta_aberta,
            student=student,
            grade2=Decimal("100.01"),
            YearSemesterReference=1,
            created_by=user,
            updated_by=user,
        )

        # Act & Assert
        with pytest.raises(ValidationError):
            enrollment.full_clean()

    def test_grade_invalid_negative_value(self, user, oferta_aberta):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE1 (Inválida)
        Valor: -50 (valor inválido negativo)
        Resultado Esperado: Rejeita com ValidationError
        """
        # Arrange
        student = StudentFactory()
        enrollment = Enrollment(
            offer=oferta_aberta,
            student=student,
            grade3=Decimal("-50"),
            YearSemesterReference=1,
            created_by=user,
            updated_by=user,
        )

        # Act & Assert
        with pytest.raises(ValidationError):
            enrollment.full_clean()


# ============================================================================
# CLASSE DE TESTES: Adicionar Aluno em Oferta
# ============================================================================


class TestOfferAddStudent:
    """
    Testa a funcionalidade de adicionar aluno em uma oferta.

    REGRA DE NEGÓCIO:
    - Apenas ofertas ABERTAS aceitam novos alunos
    - Não pode adicionar o mesmo aluno duas vezes

    CLASSES DE EQUIVALÊNCIA:
    - CE1 (Válida):   Oferta ABERTA + Aluno NÃO matriculado
    - CE2 (Inválida): Oferta FECHADA
    - CE3 (Inválida): Oferta ABERTA + Aluno JÁ matriculado
    """

    def test_add_student_to_open_offer_success(self, oferta_aberta, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE1 (Válida)
        Cenário: Adicionar aluno em oferta aberta
        Resultado Esperado: Aluno é matriculado com sucesso
        """
        # Arrange
        student = StudentFactory(course=oferta_aberta.course)

        # Act
        enrollment = oferta_aberta.add_student(student, user)

        # Assert
        assert enrollment is not None
        assert enrollment.student == student
        assert enrollment.offer == oferta_aberta
        assert Enrollment.objects.filter(
            offer=oferta_aberta,
            student=student,
        ).exists()

    def test_add_student_to_closed_offer_fails(self, oferta_fechada, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE2 (Inválida)
        Cenário: Tentar adicionar aluno em oferta fechada
        Resultado Esperado: Levanta ValidationError
        """
        # Arrange
        student = StudentFactory(course=oferta_fechada.course)

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            oferta_fechada.add_student(student, user)

        # Verifica a mensagem de erro
        assert "oferta fechada" in str(exc_info.value).lower()

    def test_add_duplicate_student_fails(self, oferta_aberta, user):
        """
        Critério: Classes de Equivalência (CE)
        Partição: CE3 (Inválida)
        Cenário: Tentar adicionar aluno que já está matriculado
        Resultado Esperado: Levanta ValidationError
        """
        # Arrange
        student = StudentFactory(course=oferta_aberta.course)
        oferta_aberta.add_student(student, user)  # Primeira matrícula

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            oferta_aberta.add_student(student, user)  # Tentativa duplicada

        # Verifica a mensagem de erro
        assert "já matriculado" in str(exc_info.value).lower()


# ============================================================================
# RESUMO DO EXEMPLO
# ============================================================================
# O QUE VOCÊ APRENDEU NESTE EXEMPLO:
#
# 1. ESTRUTURA DE TESTE:
#    - Arrange (preparar dados)
#    - Act (executar ação)
#    - Assert (verificar resultado)
#
# 2. FIXTURES:
#    - Reutilizar dados entre testes
#    - @pytest.fixture
#
# 2. CRITÉRIOS DE TESTE:
#    - Classes de Equivalência: agrupar entradas similares
#    - Valor Limite: testar valores nas bordas
#
# 4. TESTAR EXCEÇÕES:
#    - with pytest.raises(ExcecaoEsperada)
#    - Verificar mensagens de erro
#
# 5. FACTORIES:
#    - Criar objetos de teste facilmente
#    - EnrollmentFactory, OfferFactory, etc.
#
# PRÓXIMOS PASSOS:
# Agora implemente os testes nos outros arquivos seguindo este padrão!
