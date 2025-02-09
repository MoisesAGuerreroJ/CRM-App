import random
import pandas as pd

from faker import Faker

fake = Faker()
number_rows = int(input('Number of fake data rows to be generated: '))

clientes = []
with open('example_clients.sql', 'w') as f:
    f.write("INSERT INTO clientes\nVALUES\n")
    for i in range(number_rows):
        cliente = {}
        cliente['id_formulario'] = i+1
        cliente['numero_documento'] = random.randint(100000000,9999999999)
        cliente['tipo_documento'] = 'CC'
        cliente['nombre_completo'] = fake.name()
        cliente['departamento_id'] = random.choice([5,8,11,13,15,17,18,19,20,23,25,27,41,44,47,50,52,54,63,66,68,70,73,76,81,85,86,88,91,94,95,97,99])
        cliente['ciudad_id'] = 0 # TODO: Make dynamic according to departamento_id
        cliente['direccion'] = fake.address().replace('\n', ' ')
        cliente['telefono'] = fake.phone_number()[:14]
        cliente['horario'] = random.choice(['Mañana', 'Tarde', 'Noche'])
        cliente['nombre_distribuidor'] = 'Moisés Guerrero'
        cliente['telefono_distribuidor'] = '668-584-6682x754'[:14]
        cliente['promotor'] = 'Moisés Guerrero'
        cliente['telefono_promotor'] = '668-584-6682x754'[:14]
        cliente['fecha_inicio'] = random.choice(['2024-12-06', '2024-09-18', '2024-08-29'])
        cliente['fecha_vencimiento'] = None
        clientes.append(cliente)
        text = f"({cliente['id_formulario']}, {cliente['numero_documento']}, '{cliente['tipo_documento']}', '{cliente['nombre_completo']}', {cliente['departamento_id']}, {cliente['ciudad_id']}, '{cliente['direccion']}', '{cliente['telefono']}', '{cliente['horario']}', '{cliente['nombre_distribuidor']}', '{cliente['telefono_distribuidor']}', '{cliente['promotor']}', '{cliente['telefono_promotor']}', '{cliente['fecha_inicio']}', NULL)"
        if i + 1 < number_rows:
            f.write(text+',\n')
        else:
            f.write(text+';')

df_clientes = pd.DataFrame(clientes)

referidos = []
with open('example_referidos.sql', 'w') as f:
    f.write("INSERT INTO referidos\nVALUES\n")
    nro_referido = 0
    for index, i in df_clientes.iterrows():
        number_refs = random.randint(3,5)
        for j in range(number_refs):
            nro_referido += 1
            referido = {}
            referido['id'] = nro_referido
            referido['nombre'] = fake.name()
            referido['direccion'] = fake.address().replace('\n', ' ')
            referido['telefono'] = fake.phone_number()[:14]
            referido['departamento_id'] = random.choice([5,8,11,13,15,17,18,19,20,23,25,27,41,44,47,50,52,54,63,66,68,70,73,76,81,85,86,88,91,94,95,97,99])
            referido['ciudad_id'] = 0 # TODO: Make dynamic according to departamento_id
            referido['relacion_cliente'] = random.choice(["Padre/madre","Hermano(a)","Hijo(a)","Tío(a)","Primo(a)","Cuñado(a)","Suegro(a)","Ahijado(a)","Amigo(a) de la infancia","Amigo(a) del colegio","Amigo(a) del trabajo","Amigo(a) de la universidad","Amigo(a) de la iglesia","Vecino(a)","Padre/madre de amigos de sus hijos","Padrino/madrina"])
            referido['credito'] = random.choice(['Si', 'No'])
            referido['informacion_personal'] = ""
            referido['trabajo'] = random.choice(['Dia', 'Noche'])
            referido['vivienda'] = random.choice(['Dueño', 'Renta'])
            referido['conoce_royal'] = random.choice(['Si', 'No'])
            referido['cliente_id'] = i['id_formulario']
            text = f"({referido['id']}, '{referido['nombre']}', '{referido['direccion']}', '{referido['telefono']}', {referido['departamento_id']}, {referido['ciudad_id']}, '{referido['relacion_cliente']}', '{referido['credito']}', '{referido['informacion_personal']}', '{referido['trabajo']}', '{referido['vivienda']}', '{referido['conoce_royal']}', {referido['cliente_id']})"
            if index + 1 < number_rows:
                f.write(text+',\n')
            else:
                if j + 1 < number_refs:
                    f.write(text+',\n')
                else:
                    f.write(text+';')