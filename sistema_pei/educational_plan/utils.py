class NotificationEmailContent:
    @staticmethod
    def created_pei(professor_name, subject_name, student_name, year_semester):
        subject = "[Sistema PEI] Novo PEI criado."
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            "Esperamos que esteja bem.\n\n"
            "Gostaríamos de informar que um novo Plano Educacional Individualizado (PEI) "
            f"foi criado para a disciplina {subject_name} e está disponível para preenchimento no sistema.\n\n"
            "Detalhes do PEI:\n"
            f"- Disciplina: {subject_name}\n"
            f"- Aluno: {student_name}\n"
            f"- Semestre/Ano de Referência: {year_semester}\n\n"
            "Pedimos que revise as informações e preencha os campos necessários conforme as necessidades educacionais do(a) aluno(a). "
            "Caso tenha dúvidas ou precise de suporte, estamos à disposição para auxiliar.\n\n"
            "Acesse o sistema para preencher o PEI e dar seguimento ao planejamento pedagógico.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message

    @staticmethod
    def deleted_pei(professor_name, subject_name, student_name, year_semester):
        subject = "[Sistema PEI] PEI Removido"
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            "Informamos que o Plano Educacional Individualizado (PEI) para o(a) aluno(a) "
            f"{student_name} na disciplina {subject_name}, referente ao semestre/ano {year_semester}, "
            "foi removido do sistema.\n\n"
            "Caso tenha dúvidas ou precise de informações adicionais, estamos à disposição para auxiliar.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message

    @staticmethod
    def changed_history(professor_name, student_name):
        subject = "[Sistema PEI] O histórico de um aluno foi alterado!"
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            f"Informamos que o historico do o(a) aluno(a) {student_name} foi alterado no sistema."
            "para mais detalhes verifique o perfil do aluno.\n\n"
            "Caso tenha dúvidas ou precise de informações adicionais, estamos à disposição para auxiliar.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message

    @staticmethod
    def created_comment(professor_name, subject_name, student_name):
        subject = "[Sistema PEI] Novo comentário adicionado!"
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            f"Informamos que um novo comentário foi adicionado no pei do o(a) aluno(a) {student_name} na disciplina {subject_name}."
            "para mais detalhes verifique o PEI do aluno.\n\n"
            "Caso tenha dúvidas ou precise de informações adicionais, estamos à disposição para auxiliar.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message

    @staticmethod
    def created_answer(professor_name, subject_name, student_name):
        subject = "[Sistema PEI] Seu comentário foi respondido!"
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            f"Informamos que seu comentário foi respondido no pei do o(a) aluno(a) {student_name} na disciplina {subject_name}."
            "para mais detalhes verifique o PEI do aluno.\n\n"
            "Caso tenha dúvidas ou precise de informações adicionais, estamos à disposição para auxiliar.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message

    @staticmethod
    def monthly_pei(professor_name, total_pending):
        subject = "[Sistema PEI] Há PEIs para serem preenchidos"
        message = (
            f"Olá, Professor(a) {professor_name},\n\n"
            f"Informamos que há {total_pending} PEIs pendentes para serem preenchidos."
            "Por favor, revise os PEIs pendentes.\n\n"
            "Caso tenha dúvidas ou precise de informações adicionais, estamos à disposição para auxiliar.\n\n"
            "Atenciosamente,\n"
            "Equipe de Gestão Educacional\n\n"
            "---\n"
            "Esta é uma mensagem automática, por favor, não responda a este e-mail."
        )
        return subject, message
