def render_html(nome_empresa, competencia, total_cobranca, url_relacao_ativos, id_nota_fiscal):
    html_template = """

        <!DOCTYPE html>
<html lang="pt">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>

    <div style="width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: white; font-family: Inter, sans-serif;">

    <main style="width: 650px; background-color: #fff;">

        <header class="billing-email-header" style="padding: 20px; text-align: center;">
            <img src="https://i.ibb.co/C8Jp9w0/evopass-header.jpg" alt="Logo evopass" id="logo"
                style="max-width: 100%; height: auto;">
        </header>

        <article class="billing-email-body"
            style="display: flex; flex-direction: column; align-items: center; padding: 20px;">

            <section class="billing-email-section-informations" style="width: 550px;">
                <h1 class="billing-email-section-informations-acknowledgment" style="color: #FF621A; font-size: 24px;">
                    Olá, Fulano</h1>
                <p class="billing-email-section-informations-observations" style="color: #FF621A; font-size: 24px;">Este
                    é um email de faturamento, nele contém informações sobre o seu boleto, relação de ativos e nota
                    fiscal.
                    Para baixar o relação de ativos e ter acesso ao boleto, basta clicar nos botões abaixo.<br><br>Segue
                    abaixo, resumo do faturamento:</p>
                <p class="billing-email-section-informations-details">
                    <strong>Nome da empresa:</strong>""" + nome_empresa + """<br>
                    <strong>Vigência:</strong>""" + competencia + """<br>
                    <strong>Total da cobrança:</strong> R$ """ + total_cobranca + """<br>
                </p>
                <div class="billing-email-section-informations-list-buttons"
                    style="display: flex; justify-content: center; align-items: center;">
                    <a href="(função)" target="_blank" style="margin-right: 10px;">
                        <a href='""" + url_relacao_ativos + """' target="_blank">
                            <button type="button">Baixar relação de ativos</button>
                        </a>
                        <a href='http://localhost:5173/""" + id_nota_fiscal + """' target="_blank">
                            <button class="button2">
                                Baixar Nota Fiscal
                            </button>
                        </a>
                </div>
            </section>

            <section class="more-about-our-products"
                style="width: 650px; margin-top: 30px; background-color: #F3F1F1; display: flex; flex-direction: column; align-items: center;">
                <h1 class="more-about-our-products-title"
                    style="color: #FF621A; text-align: center; font-size: 24px; margin-bottom: 40px; margin-top: 50px;">
                    Um pouco mais sobre os nossos produtos</h1>
                <div class="more-about-our-products-cards"
                    style="display: flex; margin-top: 20px; margin-bottom: 20px; width: 100%; max-width: 465px; height: 153px; border: 2px solid #FF621A; border-radius: 10px;">
                    <div>
                        <img src="https://i.ibb.co/q0s0Gsz/laboral.png"
                            class="more-about-our-products-cards-img-container"
                            style="width: 100%; height: 100%; border-top-left-radius: 10px; border-bottom-left-radius: 10px;">
                    </div>
                    <div class="more-about-our-products-information-container"
                        style="display: flex; flex-direction: column; background-color: #FF621A; color: white; text-align: left; font-size: 15px; border-bottom-right-radius: 7px; border-top-right-radius: 7px;">
                        <h1 class="more-about-our-products-information-container-title"
                            style="color: #fff; height: 5px; padding-left: 20px; margin-top: 10px;">Ginástica laboral
                        </h1>
                        <p class="more-about-our-products-information-container-text"
                            style="flex: 1; padding: 10px; font-style: normal; font-weight: 300; font-size: 12px; line-height: 15px; letter-spacing: -0.05em; color: #FFFFFF; text-align: justify; line-height: 18px; margin-left: 10px; padding-right: 20px; margin-bottom: 10px;">
                            Com o Evopass você tem acesso a profissionais de educação física para realizar ginástica
                            laboral dentro da sua empresa.</p>
                    </div>
                </div>
                <div class="more-about-our-products-cards"
                    style="display: flex; margin-top: 20px; margin-bottom: 20px; width: 100%; max-width: 465px; height: 153px; border: 2px solid #FF621A; border-radius: 10px;">
                    <div>
                        <img src="https://i.ibb.co/NnJh8LG/fisioterapia.png"
                            class="more-about-our-products-cards-img-container2"
                            style="width: 100%; height: 100%; border-top-left-radius: 8px; border-bottom-left-radius: 8px;">
                    </div>
                    <div class="more-about-our-products-information-container"
                        style="display: flex; flex-direction: column; background-color: #FF621A; color: white; text-align: left; font-size: 15px; border-bottom-right-radius: 7px; border-top-right-radius: 7px;">
                        <h1 class="more-about-our-products-information-container-title"
                            style="color: #fff; height: 5px; padding-left: 20px; margin-top: 10px;">Serviços de
                            Fisioterapia</h1>
                        <p class="more-about-our-products-information-container-text"
                            style="flex: 1; padding: 10px; font-style: normal; font-weight: 300; font-size: 12px; line-height: 15px; letter-spacing: -0.05em; color: #FFFFFF; text-align: justify; line-height: 18px; margin-left: 10px; padding-right: 20px; margin-bottom: 10px;">
                            Proporcionamos vários benefícios adicionais para nossos clientes. Isso inclui colaborações
                            com profissionais de fisioterapia, nutrição, serviços de avaliação física e muito mais.</p>
                    </div>
                </div>
                <div class="more-about-our-products-cards"
                    style="display: flex; margin-top: 20px; margin-bottom: 20px; width: 100%; max-width: 465px; height: 153px; border: 2px solid #FF621A; border-radius: 10px;">
                    <div class="more-about-our-products-cards-img-container">
                        <img src="https://i.ibb.co/JB2swL9/descontos-de-parceiros.png"
                            class="more-about-our-products-cards-img-container2"
                            style="width: 100%; height: 100%; border-top-left-radius: 8px; border-bottom-left-radius: 8px;">
                    </div>
                    <div class="more-about-our-products-information-container"
                        style="display: flex; flex-direction: column; background-color: #FF621A; color: white; text-align: left; font-size: 15px; border-bottom-right-radius: 7px; border-top-right-radius: 7px;">
                        <h1 class="more-about-our-products-information-container-title"
                            style="color: #fff; height: 5px; padding-left: 20px; margin-top: 10px;">Descontos de
                            Parceiros</h1>
                        <p class="more-about-our-products-information-container-text"
                            style="flex: 1; padding: 10px; font-style: normal; font-weight: 300; font-size: 12px; line-height: 15px; letter-spacing: -0.05em; color: #FFFFFF; text-align: justify; line-height: 18px; margin-left: 10px; padding-right: 20px; margin-bottom: 10px;">
                            Cliente Evopass ganha descontos exclusivos com os nossos parceiros, São mais de 30 parceiros
                            na base.</p>
                    </div>
                </div>
                <div>
                    <button class="saiba-mais"
                        style="padding: 10px; background-color: #FF621A; color: #fff; border: none; cursor: pointer; border-radius: 8px; font-weight: bold; margin-top: 40px; margin-bottom: 0px; font-size: 18px; width: 246px; margin-bottom: 70px; margin-left: 10px;">Clique
                        aqui e saiba mais</button>
                </div>
            </section>

        </article>

        <footer class="billing-email-footer" style="display: flex; flex-direction: column; align-items: center;">

            <ul class="billing-email-footer-list-buttons"
                style="list-style: none; display: flex; flex-direction: row; justify-content: space-evenly; align-items: center; width: 200px; margin-right: 65px; margin-top: 30px;">
                <li class="billing-email-footer-list-buttons-button-link">
                    <a href="https://www.instagram.com/evopassbr/" target="_blank">
                        <img src="https://i.ibb.co/QnfJPK7/instagram.png" alt="instagram"
                            style="width: 40px; height: 40px;">
                    </a>
                </li>
                <li class="billing-email-footer-list-buttons-button-link">
                    <a href="https://www.evopass.app.br/" target="_blank">
                        <img src="https://i.ibb.co/hCqTcND/logotipo-do-linkedin.png" alt="linkedin"
                            style="width: 40px; height: 40px;">
                    </a>
                </li>
                <li class="billing-email-footer-list-buttons-button-link">
                    <a href="https://www.evopass.app.br/pol%C3%ADtica-de-privacidade" target="_blank">
                        <img src="https://i.ibb.co/z4Ybx0h/enviar.png" alt="enviar" style="width: 40px; height: 40px;">
                    </a>
                </li>
            </ul>

            <div>
                <h2 class="footer-title" style="color: #FF621A; font-size: 24px; margin-top: 70px;">Abraços</h2>
                <h2 class="footer-subtitle" style="color: #FF621A; font-size: 24px;">Equipe Evopass</h2>
                <p class="footer-paragraph" style="font-size: 20px; font-weight: lighter;">Por favor, pedimos que você
                    não responda esse e-mail,
                    pois se trata de uma mensagem automática e não é possível dar continuidade com seu atendimento por
                    aqui.</p>
                <p class="footer-instructions"
                    style="font-family: Inter, sans-serif; font-style: normal; font-weight: 300; font-size: 16px; line-height: 120%; margin-top: 50px; margin-bottom: 50px;">
                    Caso ainda tenha dúvidas, acesse <u>Ajuda</u> diretamente no nosso site.</p>
                <img src="https://i.ibb.co/c8B193f/footer.png" alt="footer" class="footer-image" style="width: 100%;">
            </div>

        </footer>

    </main>
    
    </div>


</body>

</html>

    """

    return html_template