from flask import Flask, render_template, url_for, flash, redirect, request, Response
from python_graphql_client import GraphqlClient
import base64

client = GraphqlClient(endpoint="http://127.0.0.1:8000/graphql/")

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html', title="Inicio")


@app.route('/listar', methods=['GET', 'POST'])
def listar():
    if request.method == 'POST':
        dato = request.form['myInput']
        query = 'query{\nallAsociados(nombre_Icontains: "'
        query = query + str(dato)
        query = query + '"){\nedges{\nnode{\nid\nnombre\napellido\nfechaNacimiento\nfechaRenmem\ntelefono\n\
                            direccion\ncorreo\nespecialidad{\nid\ncategoria\n}\nsubespecialidad{\nid\ncategoria\
                            \n}\n}\n}\n}\n}'

    else:
        query="""
        query{
  allAsociados{
    edges{
      node{
        id
        nombre
        apellido
        fechaNacimiento
        fechaRenmem
        telefono
        direccion
        correo
        especialidad{
            id
            categoria
        }
        subespecialidad{
            id
            categoria
        }
      }
    }
  }
}
        """
    data = client.execute(query=query, verify=False)
    print(query)
    #for i in data['data']['allAsociados']['edges']:
    #    print(i['node']['nombre'])
    return render_template('listado.html', title="Listado", data=data['data']['allAsociados']['edges'])
    


@app.route("/acerca")
def acerca():
    return render_template('acerca.html', title='Acerca')


@app.route("/eliminar/<id>")
def eliminar(id):
    #print(id)
    aux = str(base64.b64decode(id))
    div = aux.split(':')
    div = div[1].split("'")
    query = "mutation{\ndeleteAsociado(id:"+str(div[0])+"){\nasociado{\nnombre\n}\n}\n}"
    #print(query)
    client.execute(query=query)
    return redirect(url_for('listar'))


@app.route("/ingresodatos", methods=['GET', 'POST'])
def ingresodatos():
    query = """
    query{
  allEspecialidades{
    edges{
      node{
        id
        categoria
      }
    }
  }
}
    """
    data = client.execute(query=query, verify=False)
    especialidades = data['data']['allEspecialidades']['edges']

    query = """
    query{
  allSubespecialidades{
    edges{
      node{
        id
        categoria
      }
    }
  }
}
    """
    data = client.execute(query=query, verify=False)
    subespecialidades = data['data']['allSubespecialidades']['edges']

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dianac = request.form["dianac"]
        mesnac = request.form["mesnac"]
        anionac = request.form["anionac"]
        diaren = request.form["diaren"]
        mesren = request.form["mesren"]
        anioren = request.form["anioren"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        aux = str(base64.b64decode(request.form["especialidad"]))
        div = aux.split(':')
        div = div[1].split("'")
        especialidad = int(div[0])
        aux = str(base64.b64decode(request.form["subespecialidad"]))
        div = aux.split(':')
        div = div[1].split("'")
        subespecialidad = int(div[0])

        query1 = 'mutation{\ncreateAsociado(nombre: "'
        query1 = query1 + str(nombre)+'", apellido: "'
        query1 = query1 + str(apellido)+'", fechaRenmem: "'
        query1 = query1 + str(anioren)+'-'+str(mesren)+'-'+str(diaren)+ 'T00:00:00Z", fechaNacimiento: "'
        query1 = query1 + str(anionac)+'-'+str(mesnac)+'-'+str(dianac)+ 'T00:00:00Z", direccion:"'
        query1 = query1 + str(direccion)+ '",telefono: '
        query1 = query1 + str(telefono) + ', correo: "'
        query1 = query1 + str(correo)+'", especialidad: '
        query1 = query1 + str(especialidad) + ', subespecialidad: '
        query1 = query1 + str(subespecialidad)+ '){\nasociado{\nid\nnombre\napellido\nfechaRenmem\nfechaNacimiento\n\
      direccion\ntelefono\ncorreo\nespecialidad{\nid\ncategoria\n}\nsubespecialidad{\nid\ncategoria\n}\n}\n}\n}'
        print('Query be like:', query1)
        client.execute(query=query1)

        return redirect(url_for('listar'))
    return render_template('ingresodatos.html', title='Ingreso de Datos', especialidades=especialidades, subespecialidades = subespecialidades)