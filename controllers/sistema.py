# controllers/sistema.py - Lógica de controle principal e gestão de produtos
import json
import os
from models.produto import Produto
from models.caixa import Caixa
from models.carrinho import Carrinho
from models.pagamento import Pagamento
from utils.io_helpers import ler_inteiro, ler_float, ler_texto
from utils.logging_simple import log

class Sistema:
    # Nome do arquivo onde os dados de produtos serão salvos/carregados
    ARQUIVO_PRODUTOS = "data/produtos.json"

    def __init__(self):
        # 1. Carrega os produtos da persistência.
        # Se o arquivo não existir ou estiver vazio, self.produtos será uma lista vazia ([]).
        self.produtos = self.carregar_produtos()
        
        if not self.produtos:
             print("Estoque inicializado vazio. Por favor, adicione produtos via menu 'Gerenciar produtos'.")

        # 2. Inicializa o Caixa
        self.caixa = Caixa()

    # ********************************
    # Métodos de Persistência (Produtos) (código omitido, sem alteração)
    # ********************************

    # Carrega a lista de Produtos do arquivo JSON
    def carregar_produtos(self) -> list[Produto]:
        produtos = []
        if os.path.exists(self.ARQUIVO_PRODUTOS):
            try:
                with open(self.ARQUIVO_PRODUTOS, "r", encoding="utf-8") as f:
                    # Trata arquivo JSON vazio/inválido
                    try:
                        produtos_data = json.load(f)
                    except json.JSONDecodeError:
                        log(f"ERRO: O arquivo de persistência {self.ARQUIVO_PRODUTOS} está vazio ou corrompido.")
                        return [] # Retorna lista vazia em caso de erro
                    except EOFError:
                        return [] # Retorna lista vazia se for um arquivo vazio

                    for d in produtos_data:
                        produtos.append(Produto.from_dict(d))
            except Exception as e:
                log(f"ERRO ao carregar produtos: {e}")
                return []
        return produtos

    # Salva o estado atual da lista de Produtos no arquivo JSON
    def salvar_produtos(self):
        os.makedirs(os.path.dirname(self.ARQUIVO_PRODUTOS), exist_ok=True)
        produtos_data = [p.to_dict() for p in self.produtos]
        try:
            with open(self.ARQUIVO_PRODUTOS, "w", encoding="utf-8") as f:
                json.dump(produtos_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            # Trata erros de escrita e loga
            log(f"ERRO CRÍTICO: Falha ao salvar produtos em {self.ARQUIVO_PRODUTOS}. {e}")
            print("ERRO: Falha na persistência dos dados de produtos. Consulte o log.")

    # MANTIDO: O método de inicializar produtos de exemplo é mantido, mas não é mais chamado no __init__
    def _inicializar_produtos_exemplo(self):
        self.produtos.append(Produto(100, "Arroz Tio João 5kg", 25.99, 50, 5))
        self.produtos.append(Produto(201, "Feijão Preto Tipo 1", 8.50, 40, 5))
        self.produtos.append(Produto(305, "Leite Integral 1L", 4.99, 100, 10))
        self.produtos.append(Produto(410, "Pão de Forma Tradicional", 6.80, 20, 3))
        self.salvar_produtos() # Salva a lista inicial

    # ********************************
    # Métodos de Busca (código omitido, sem alteração)
    # ********************************

    # Busca um produto pelo código
    def buscar_produto(self, codigo: int) -> Produto | None:
        try:
            codigo = int(codigo)
            for produto in self.produtos:
                if produto.codigo == codigo:
                    return produto
            return None
        except ValueError:
            print("Código deve ser um número inteiro.")
            return None
    
    # NOVO MÉTODO: Gera o próximo código de produto disponível
    def _gerar_novo_codigo(self) -> int:
        if not self.produtos:
            # Se a lista estiver vazia, começa com o código 100
            return 100
        
        # Encontra o maior código existente
        maior_codigo = max(p.codigo for p in self.produtos)
        # Retorna o próximo código sequencial
        return maior_codigo + 1

    # ********************************
    # Menus e Gerenciamento
    # ********************************

    # Menu para gerenciar produtos (código omitido, sem alteração)
    def menu_gerenciar_produtos(self):
        while True:
            print("\n===== GERENCIAR PRODUTOS =====")
            print("[1] Adicionar novo produto")
            print("[2] Listar todos os produtos (e alertas de estoque)")
            print("[3] Editar produto (preço/estoque/minimo)")
            print("[4] Deletar produto")
            print("[5] Voltar ao Menu Principal")

            opc = ler_texto("Escolha uma opção: ")

            if opc == "1":
                self._adicionar_produto()
            elif opc == "2":
                self._listar_produtos_com_alerta()
            elif opc == "3":
                self._editar_produto()
            elif opc == "4":
                self._deletar_produto()
            elif opc == "5":
                break
            else:
                print("Opção inválida. Escolha 1, 2, 3, 4 ou 5.")

    # Adiciona um novo produto ao estoque (MODIFICADO)
    def _adicionar_produto(self):
        print("\n--- ADICIONAR PRODUTO ---")
        
        # Gera e exibe o código automaticamente
        codigo = self._gerar_novo_codigo()
        print(f"Código do novo produto gerado automaticamente: {codigo}")
        
        # Remove a checagem de código existente, pois o código é sempre novo.
        # Remove a solicitação de entrada do código pelo usuário.

        nome = ler_texto("Digite o nome do produto: ")
        preco = ler_float("Digite o preço unitário (ex: 12.50): ")
        estoque = ler_inteiro("Digite a quantidade inicial em estoque: ")
        estoque_minimo = ler_inteiro("Digite o estoque mínimo para alerta: ")

        try:
            novo_produto = Produto(codigo, nome, preco, estoque, estoque_minimo)
            self.produtos.append(novo_produto)
            self.salvar_produtos()
            print(f"Produto '{nome}' (Cód: {codigo}) adicionado com sucesso.")
        except Exception as e:
            print(f"ERRO ao criar produto: {e}")
            log(f"Falha na criação de produto. Código: {codigo}, Erro: {e}")

    # Lista todos os produtos, destacando aqueles com estoque baixo (código omitido, sem alteração)
    def _listar_produtos_com_alerta(self):
        if not self.produtos:
            print("\nNenhum produto cadastrado.")
            return

        print("\n--- LISTA DE PRODUTOS ---")
        for produto in self.produtos:
            alerta = " [ALERTA: ESTOQUE BAIXO]" if produto.estoque_baixo() else ""
            print(f"{produto}{alerta}")

    # Permite editar preço, estoque e estoque mínimo de um produto existente (código omitido, sem alteração)
    def _editar_produto(self):
        self._listar_produtos_com_alerta()
        if not self.produtos:
            return

        print("\n--- EDITAR PRODUTO ---")
        codigo = ler_inteiro("Digite o código do produto a ser editado: ")
        produto = self.buscar_produto(codigo)

        if not produto:
            print(f"Produto com código {codigo} não encontrado.")
            return

        print(f"Produto selecionado: {produto.nome}")

        # Edição de Preço
        novo_preco = ler_float(f"Novo preço (R$ {produto.preco:.2f} atual - '0' para manter): ")
        if novo_preco > 0:
            produto._preco = novo_preco
            print("Preço atualizado.")

        # Edição de Estoque
        nova_quantidade = ler_inteiro(f"Nova quantidade em estoque ({produto.estoque} atual - '0' para manter): ")
        if nova_quantidade > 0:
            try:
                produto.atualizar_estoque(nova_quantidade)
                print("Estoque atualizado.")
            except ValueError as e:
                print(f"ERRO: {e}")

        # Edição de Estoque Mínimo
        novo_minimo = ler_inteiro(f"Novo estoque mínimo ({produto.estoque_minimo} atual - '0' para manter): ")
        if novo_minimo > 0:
            try:
                produto.atualizar_estoque_minimo(novo_minimo)
                print("Estoque mínimo atualizado.")
            except ValueError as e:
                print(f"ERRO: {e}")

        self.salvar_produtos()
        print(f"Produto {produto.nome} editado e salvo.")
    
    # NOVO MÉTODO: Permite deletar um produto pelo código (código omitido, sem alteração)
    def _deletar_produto(self):
        self._listar_produtos_com_alerta()
        if not self.produtos:
            return

        print("\n--- DELETAR PRODUTO ---")
        codigo = ler_inteiro("Digite o código do produto a ser DELETADO: ")
        produto = self.buscar_produto(codigo)

        if not produto:
            print(f"Produto com código {codigo} não encontrado.")
            return

        confirmacao = ler_texto(f"Tem certeza que deseja DELETAR '{produto.nome}' (S/N)? ").strip().upper()

        if confirmacao == 'S':
            try:
                self.produtos.remove(produto)
                self.salvar_produtos()
                print(f"Produto {produto.nome} (código {codigo}) DELETADO com sucesso.")
                log(f"Produto deletado: {produto.nome} (cód: {codigo})")
            except ValueError:
                 print(f"ERRO: Produto {produto.nome} não encontrado na lista (falha interna).")
            except Exception as e:
                print(f"ERRO ao deletar produto: {e}")
                log(f"Falha ao deletar produto. Código: {codigo}, Erro: {e}")
        else:
            print("Operação de deleção cancelada.")


    # ********************************
    # Caixa / Atendimento (código omitido, sem alteração)
    # ********************************

    # Inicia um novo ciclo de atendimento ao cliente
    def abrir_caixa_e_atender(self):
        carrinho = Carrinho()
        print("\n===== CAIXA ABERTO - INICIANDO ATENDIMENTO =====")

        while True:
            self._listar_produtos_com_alerta() # Lista produtos com alerta
            print("\n--- ATENDIMENTO ---")
            print("[A] Adicionar produto")
            print("[R] Remover produto do carrinho")
            print("[F] Finalizar compra (Pagamento)")
            print("[C] Cancelar compra e Fechar Caixa")

            opc = ler_texto("Escolha uma opção: ").upper()

            if opc == "A":
                self._adicionar_ao_carrinho(carrinho)
            elif opc == "R":
                self._remover_do_carrinho(carrinho)
            elif opc == "F":
                if carrinho.vazio():
                    print("O carrinho está vazio. Adicione produtos primeiro.")
                else:
                    self._finalizar_compra(carrinho)
                    break # Sai do loop de atendimento após a venda
            elif opc == "C":
                self._cancelar_compra(carrinho)
                break # Sai do loop de atendimento
            else:
                print("Opção inválida. Use A, R, F ou C.")

        # Após fechar a compra ou cancelar, gera o fechamento do caixa
        self.caixa.fechamento()
        print("===== CAIXA FECHADO =====")


    # Adiciona produto ao carrinho, interagindo com o usuário
    def _adicionar_ao_carrinho(self, carrinho: Carrinho):
        codigo = ler_inteiro("Digite o código do produto: ")
        produto = self.buscar_produto(codigo)

        if not produto:
            print(f"Produto com código {codigo} não encontrado.")
            return

        print(f"Produto encontrado: {produto}")
        quantidade = ler_inteiro(f"Quantidade a adicionar (Máx: {produto.estoque}): ")

        try:
            carrinho.adicionar(produto, quantidade)
            print(f"{quantidade}x {produto.nome} adicionado ao carrinho.")
            self._mostrar_resumo_carrinho(carrinho)
            self.salvar_produtos() # Salva novo estado do estoque
        except ValueError as e:
            print(f"ERRO: {e}")
            log(f"Falha ao adicionar ao carrinho. Produto: {codigo}, Erro: {e}")


    # Remove produto do carrinho, interagindo com o usuário
    def _remover_do_carrinho(self, carrinho: Carrinho):
        if carrinho.vazio():
            print("O carrinho está vazio.")
            return

        # Melhoria de visualização: garante que o usuário veja os códigos antes de digitar
        self._mostrar_resumo_carrinho(carrinho, exibir_codigo=True)

        codigo = ler_inteiro("Digite o código do produto para remover: ")
        produto = self.buscar_produto(codigo)

        if not produto:
            print(f"Produto com código {codigo} não encontrado.")
            return

        # Busca o objeto Produto que está no carrinho (usando __eq__ e __hash__)
        produto_no_carrinho = next((p for p in carrinho.listar_itens() if p[0].codigo == codigo), None)

        if not produto_no_carrinho:
             print(f"Produto {produto.nome} não está no carrinho.")
             return

        qtd_no_carrinho = produto_no_carrinho[1]
        quantidade = ler_inteiro(f"Quantidade a remover (Máx: {qtd_no_carrinho}): ")

        try:
            carrinho.remover(produto, quantidade)
            print(f"{quantidade}x {produto.nome} removido do carrinho.")
            self._mostrar_resumo_carrinho(carrinho)
            self.salvar_produtos() # Salva novo estado do estoque
        except ValueError as e:
            print(f"ERRO: {e}")
            log(f"Falha ao remover do carrinho. Produto: {codigo}, Erro: {e}")


    # Finaliza a compra processando pagamento e registrando venda (código omitido, sem alteração)
    def _finalizar_compra(self, carrinho: Carrinho):
        print("\n--- FINALIZAR COMPRA ---")
        total_bruto = carrinho.calcular_total()
        print(f"Total Bruto da Compra: R$ {total_bruto:.2f}")

        # Aplicação de Cupom
        cupom = ler_texto("Aplicar cupom (opcional, ENTER para pular): ")
        pagamento = Pagamento(total_bruto, cupom)

        # Escolha da forma de pagamento
        while True:
            print("\n--- FORMAS DE PAGAMENTO ---")
            print("[1] Dinheiro/PIX (10% desconto)")
            print("[2] Débito (5% desconto)")
            print("[3] Crédito 1x (Sem desconto)")
            print("[4] Crédito 2x (+5%)")
            print("[5] Crédito 3x (+10%)")
            print("[6] Crédito 4x (+15%)")

            try:
                opcao_pagamento = ler_inteiro("Escolha a forma de pagamento (1-6): ")
                pagamento.calcular_pagamento(opcao_pagamento)
                break
            except ValueError as e:
                print(f"ERRO: {e}. Tente novamente.")

        # Exibe resumo final e registra a venda
        print("\n===== RESUMO DA VENDA =====")
        print(f"Total Bruto: R$ {total_bruto:.2f}")
        print(f"Forma de Pagamento: {pagamento.descricao}")
        print(f"TOTAL A PAGAR: R$ {pagamento.valor_final:.2f}")
        print("===========================")

        self.caixa.registrar_venda(
            total_compra=pagamento.valor_final,
            itens_vendidos=carrinho.total_itens(),
            forma=pagamento.descricao,
            cupom=pagamento.cupom if pagamento.cupom else "N/A"
        )
        print("Venda registrada com sucesso!")


    # Desfaz a compra, devolvendo todos os itens ao estoque (código omitido, sem alteração)
    def _cancelar_compra(self, carrinho: Carrinho):
        print("\n--- COMPRA CANCELADA ---")
        # Itera sobre os itens do carrinho e remove cada um para devolver ao estoque
        for produto, quantidade in list(carrinho.listar_itens()):
            try:
                # O método remover trata de devolver o estoque
                carrinho.remover(produto, quantidade)
                log(f"Devolvendo ao estoque: {quantidade}x {produto.nome}")
            except Exception as e:
                log(f"ERRO CRÍTICO ao reverter estoque de {produto.codigo}: {e}")
                print(f"ERRO: Falha ao reverter estoque do produto {produto.nome}.")

        self.salvar_produtos() # Salva novo estado do estoque
        print("O carrinho foi esvaziado e o estoque revertido.")


    # Exibe o estado atual do carrinho (código omitido, sem alteração)
    def _mostrar_resumo_carrinho(self, carrinho: Carrinho, exibir_codigo: bool = False):
        print("\n[ CARRINHO ]")
        if carrinho.vazio():
            print("Vazio.")
        else:
            for produto, quantidade in carrinho.listar_itens():
                # Aprimoramento da visualização para exibir o código
                codigo_str = f" [Cód: {produto.codigo}]" if exibir_codigo else ""
                print(f"  - {quantidade}x {produto.nome}{codigo_str} (R$ {produto.preco:.2f} cada)")
            print(f"  TOTAL BRUTO: R$ {carrinho.calcular_total():.2f}")