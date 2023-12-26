def render_html(nome_empresa, competencia, total_cobranca, url_relacao_ativos, id_nota_fiscal):
    html_template = """
        <div style="display: flex; flex-direction: column; align-items: center;">
            <main style="display: flex; flex-direction: column; align-items: center;width: 650px; background-color: #99989846;">
                <header class="billing-email-header" style="padding: 20px; text-align: center;">
                    <img src="https://i.ibb.co/T1FcVfM/Imagem1.png" alt="Logo evopass" style="max-width: 100%;">
                </header>
                <article class="billing-email-body"
                    style="display: flex; flex-direction: column; align-items: center; padding: 20px;">
                    <section class="billing-email-section-informations" style="width: 550px;">
                        <h1 class="billing-email-section-informations-acknowledgment" style="color: #0066cc;">Obrigado por
                            escolher a Evopass!</h1>
                        <p class="billing-email-section-informations-observations"
                            style="text-align: justify; margin-top: 30px;">
                            Este é um email de faturamento, nele contém informações sobre o seu boleto, relação de ativos e nota
                            fiscal.
                            Para baixar o relação de ativos e ter acesso ao boleto, basta clicar nos botões abaixo.
                            <br>
                            <br>
                            Segue abaixo, resumo do faturamento:
                        </p>
                        <ul class="billing-email-section-informations-details" style="text-align: justify; margin-top: 10px;">
                            <li>Nome da empresa: """ + nome_empresa + """</li>
                            <li>Competência: """ + competencia + """</li>
                            <li>Total da cobrança: R$ """ + total_cobranca + """</li>
                        </ul>
                        <div class="billing-email-section-informations-list-buttons"
                            style="display: flex; flex-direction: row; justify-content: space-evenly; margin-top: 20px;">
                            <a href='""" + url_relacao_ativos + """' target="_blank" style="margin-right: 10px; text-decoration: none;">
                                <button type="button"
                                    style="padding: 10px 20px; background-color: #0066cc; color: #fff; border: none; cursor: pointer;">Baixar
                                    relação de ativos</button>
                            </a>
                            <a href='https://nfse-evopass.web.app/""" + id_nota_fiscal + """' target="_blank" style="text-decoration: none;">
                                <button
                                    style="padding: 10px 20px; background-color: #0066cc; color: #fff; border: none; cursor: pointer;">Baixar
                                    nota fiscal</button>
                            </a>
                        </div>
                    </section>
                    <section class="more-about-our-products" style="width: 500px; margin-top: 30px;">
                        <h1 class="more-about-our-products-title" style="color: #0066cc;">Um pouco mais sobre os nossos produtos
                        </h1>
                        <div class="more-about-our-products-cards" style="height: 150px; display: flex; margin-top: 20px;">
                            <div class="more-about-our-products-cards-img-container" style="flex: 0 0 30%;">
                                <img src="https://sesirs.org.br/sites/default/files/styles/2x1_lg/public/paragraphs--image-top/istock-878674766_2196_x_1366.jpg?itok=0JHsdShU"
                                    alt="" style="width: 100%;">
                            </div>
                            <div class="more-about-our-products-information-container"
                                style="flex: 0 0 70%; padding-left: 20px;">
                                <h1 class="more-about-our-products-information-container-title" style="color: #333;">Ginática
                                    laboral</h1>
                                <p class="more-about-our-products-information-container-text"
                                    style="width: 90%; text-align: justify; margin-top: 15px;">
                                    Com o Evopass você tem acesso a profissionais de educação física para realizar ginástica
                                    laboral dentro da sua empresa.
                                </p>
                            </div>
                        </div>
                        <div class="more-about-our-products-cards" style="height: 150px; display: flex; margin-top: 20px;">
                            <div class="more-about-our-products-cards-img-container" style="flex: 0 0 30%;">
                                <img src="https://www.alvita.com.br/images/services/servicos-fisioterapia.png" alt=""
                                    style="width: 100%;">
                            </div>
                            <div class="more-about-our-products-information-container"
                                style="flex: 0 0 70%; padding-left: 20px;">
                                <h1 class="more-about-our-products-information-container-title" style="color: #333;">Serviços de
                                    Fisioterapia</h1>
                                <p class="more-about-our-products-information-container-text"
                                    style="width: 90%; text-align: justify; margin-top: 15px;">
                                    Proporcionamos benefícios adicionais para nossos clientes. Isso inclui colaborações com
                                    profissionais de fisioterapia, nutrição, serviços de avaliação física e muito mais.
                                </p>
                            </div>
                        </div>
                        <div class="more-about-our-products-cards" style="height: 150px; display: flex; margin-top: 20px;">
                            <div class="more-about-our-products-cards-img-container" style="flex: 0 0 30%;">
                                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9PyjYZIpgtilbhfaAK5jKppJKmX3QMMIsmg&usqp=CAU"
                                    alt="" style="width: 100%;">
                            </div>
                            <div class="more-about-our-products-information-container"
                                style="flex: 0 0 70%; padding-left: 20px;">
                                <h1 class="more-about-our-products-information-container-title" style="color: #333;">Descontos
                                    com parceiros</h1>
                                <p class="more-about-our-products-information-container-text"
                                    style="width: 90%; text-align: justify; margin-top: 15px;">
                                    Cliente Evopass ganha descontos exclusivos com os nossos parceiros, São mais de 30 parceiros
                                    na base.
                                </p>
                            </div>
                        </div>
                    </section>
                </article>
                <hr>
                <footer class="billing-email-footer" style="padding: 20px;">
                    <ul class="billing-email-footer-list-buttons"
                        style="list-style: none; display: flex; flex-direction: row; justify-content: space-evenly;">
                        <li class="billing-email-footer-list-buttons-button-link" style="color: #0066cc; cursor: pointer;">
                            <a href="https://www.instagram.com/evopassbr/" target="_blank" style="text-decoration: none;">
                                INSTAGRAM
                            </a>
                        </li>
                        <li class="billing-email-footer-list-buttons-button-link" style="color: #0066cc; cursor: pointer;">
                            <a href="https://www.evopass.app.br/" target="_blank" style="text-decoration: none;">
                                NOSSO SITE
                            </a>
                        </li>
                        <li class="billing-email-footer-list-buttons-button-link" style="color: #0066cc; cursor: pointer;">
                            <a href="https://www.evopass.app.br/pol%C3%ADtica-de-privacidade" target="_blank"
                                style="text-decoration: none;">
                                TERMOS
                            </a>
                        </li>
                    </ul>
                </footer>
            </main>
        </div>
    """
    return html_template