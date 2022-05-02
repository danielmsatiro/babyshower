from app.models.email_model import EmailModel


def email_to_new_user(nickname: str, email: str) -> None:
    """Send an email to the user confirming their registration

    Args:
        nickname (str): User nickname
        email (str): User email
    """
    subject = 'Bem-vindo à BabyShowers!'
    message = f"""
        <h2>Oi, {nickname}!</h2>
        <h1>Bem-vindo à comunidade BabyShowers</h1>
        <p>Estamos muito felizes por você fazer parte desta comunidade que cresce a cada instante.</p>
        <span>E-mail gerado automaticamente, não responda.</span>
    """
    
    my_email = EmailModel(email, subject, message)
    my_email.send_email()


def email_new_product(owner: str, title: str, email: str) -> None:
    """Send an email to the user confirming their registration

    Args:
        owner (str): Product owner nickname
        title (str): Product title
        email (str): Product owner email
    """
    subject = 'BabyShowers: Novo produto cadastrado!'
    message = f"""
        <h2>Oi, {owner}!</h2>
        <p>Seu produto "{title}" foi cadastrado com sucesso!</p>
        <span>E-mail gerado automaticamente, não responda.</span>
    """
    
    my_email = EmailModel(email, subject, message)
    my_email.send_email()


def email_new_question(owner: str, title: str, email: str, lead: str, question: str) -> None:
    """Send an email to the product owner stating the question asked, about which product and who asked the question.
    Args:
        owner (str): Product owner nickname
        title (str): Product title
        email (str): Product owner email
        lead (str): Lead nickname
        question (str): The question
    """
    subject = 'BabyShowers: Nova pergunta!'
    message = f"""
        <h1>Oi, {owner}!</h1>
        <p>O usuário "{lead}" enviou uma pergunta sobre o produto {title}.</p>
        <p>"{question}"</p>
        <span>E-mail gerado automaticamente, não responda.</span>
    """
    
    my_email = EmailModel(email, subject, message)
    my_email.send_email()


def email_new_answer(lead: str, title: str, email: str, owner: str, answer: str) -> None:
    """Send an email to the product owner stating the question asked, about which product and who asked the question.
    Args:
        lead (str): Lead nickname
        title (str): Product title
        email (str): Lead email
        owner (str): Product owner nickname
        answer (str): The answer
    """
    subject = 'BabyShowers: Nova resposta!'
    message = f"""
        <h1>Oi, {lead}!</h1>
        <p>O usuário "{owner}" enviou uma resposta sobre o produto {title}.</p>
        <p>"{answer}"</p>
        <span>E-mail gerado automaticamente, não responda.</span>
    """
    
    my_email = EmailModel(email, subject, message)
    my_email.send_email()