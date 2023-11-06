from fastapi import FastAPI

app = FastAPI()

@app.get("/",tags=['ROOT'])
async def root()->dict:
    return {"ping":"pong"}


#Get --> Read Todo
#Post --> Creat Todo
#Pull --> Update Todo
#Delete --> Delete Todo


@app.get('/todo',tags=['todos'])
async def get_todo()-> dict:
    return{"data":todos}


@app.post('/todo',tags=['todos'])
async def add_todo(todo:dict):
    todos.append(todo)
    return {
        "data":"Data added sucessfullt"
    }
    
@app.put('/todo/{id}',tags=['todos'])
async def update_todo(id:int,body:dict) ->dict:
    for todo in todos:
        if int(todo['id']) == id:
            todo['Acvtivity'] = body['Acvtivity']
            return {
                "data":f"updated the id {id} sussecfully "
            }
    return {
        "data":f"id number is not found"
    }
    
@app.delete('/todo',tags=['todos'])
async def delete_todo(id:int)-> dict:
    for todo in todos:
        if int(todo['id']) == id:
            todos.remove(todo)
            return {
                "data":f"id with {id} is removed sussesfully"
            }
    
    return {
                "data":f"id with {id} is not foun"
            }
        



todos = [
    {
        "id":"1",
        "Acvtivity":"jogging two hous"
    },
     {
        "id":"2",
        "Acvtivity":"write 3 pages"
    },
    
]