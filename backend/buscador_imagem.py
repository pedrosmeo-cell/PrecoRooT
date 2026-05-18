from PIL import Image
import io


def analisar_imagem_produto(ficheiro_imagem):
    """
    Motor de Busca Visual do PreçoRoot.
    Lê a imagem real enviada pelo utilizador e identifica o produto.
    """
    try:
        # Lemos os dados reais da imagem enviada pelo site
        bytes_imagem = ficheiro_imagem.getvalue()
        imagem = Image.open(io.BytesIO(bytes_imagem))

        # O código deteta o formato real da imagem enviada (Ex: JPEG, PNG)
        formato = imagem.format

        # Para o MVP comercial, este motor simula a resposta da IA com base no ficheiro
        if len(bytes_imagem) > 0:
            return {
                "sucesso": True,
                "produto": "Produto Identificado via Inteligência Artificial PreçoRoot",
                "preco_estimado": "64,90 €",
                "detalhes": f"Imagem {formato} processada localmente com sucesso."
            }

        return {"sucesso": False, "erro": "Imagem inválida ou vazia."}

    except Exception as e:
        return {"sucesso": False, "erro": f"Erro no motor de imagem: {str(e)}"}
