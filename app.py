from flask import Flask, render_template, url_for, flash, redirect, request, Response
from python_graphql_client import GraphqlClient

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
        especialidad = request.form["especialidad"]
        subespecialidad = request.form["subespecialidad"]

        query = 'mutation{\ncreateAsociado(nombre: "'
        query = query + str(nombre)+'", apellido: "'
        query = query + str(apellido)+'", fechaRenmem: "'
        query = query + str(anioren)+'-'+str(mesren)+'-'+str(diaren)+ '", fechaNacimiento: "'
        query = query + str(anionac)+'-'+str(mesnac)+'-'+str(dianac)+ '", direccion:"'
        query = query + str(direccion)+ '",telefono: '
        query = query + str(telefono) + ', correo: "'
        query = query + str(correo)+'", especialidad: '
        query = query + str(especialidad) + ', subespecialidad: '
        query = query + str(subespecialidad)+ '){\nasociado{\nid\nnombre\napellido\nfechaRenmem\nfechaNacimiento\n\
      direccion\ntelefono\ncorreo\nespecialidad{\nid\ncategoria\n}\nsubespecialidad{\nid\ncategoria\n}\n}\n}\n}'

        print(query)
        data=client.execute(query=query, verify=False)

        return redirect(url_for('listar'))
    return render_template('ingresodatos.html', title='Ingreso de Datos', especialidades=especialidades, subespecialidades = subespecialidades)