import base64

def criarImagem(code,nome):

    file = code.encode('utf-8')
    # byte = file.read() 
    # file.close() 
    
    decodeit = open(f'Media/{nome}.png', 'wb') 
    decodeit.write(base64.b64decode((file))) 
    decodeit.close() 