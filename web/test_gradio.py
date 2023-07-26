import gradio as gr
import time
demo = gr.Blocks()

def trans(msg,states:list,req:gr.Request):
    states.append({"time":time.asctime(time.localtime()),"msg":msg })
    return states,states,req.request.client

with demo:
    msg = gr.Text('hi')
    gr.Code()
    states = gr.State([])
    gr.Markdown("""          
                """)
    out = gr.Text()

    gr.Video()
    gr.Button().click(trans,[msg,states],[states,gr.Json(),gr.Text()])
if __name__ == "__main__":
    demo.launch()
