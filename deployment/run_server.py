from flask import Flask, render_template, request
import torch
import random
import numpy as np
from utils import header, add_content, box
from wtforms import Form, TextField, validators, SubmitField
from GPT2.model import (GPT2LMHeadModel)
from GPT2.utils import load_weight
from GPT2.config import GPT2Config
from GPT2.sample import sample_sequence
from GPT2.encoder import get_encoder


# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = TextField("Enter a seed sentence:", validators=[
                     validators.InputRequired()])

    # Submit button
    submit = SubmitField("Enter")


def text_generator(
    seed,
    unconditional=False,
    nsamples=1,
    batch_size=-1,
    length=-1,
    temperature=0.7,
    top_k=40):

    enc = get_encoder()
    context_tokens = enc.encode(seed)

    if batch_size == -1:
        batch_size = 1
    assert nsamples % batch_size == 0

    if length == -1:
        length = config.n_ctx // 2
    elif length > config.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % config.n_ctx)

    out = sample_sequence(
        model=model,
        length=length,
        context=context_tokens if not unconditional else None,
        start_token=enc.encoder['<|endoftext|>'] if unconditional else None,
        batch_size=batch_size,
        temperature=temperature,
        top_k=top_k,
        device=device
    )

    text = ''

    out = out[:, len(context_tokens):].tolist()
    for i in range(batch_size):
        text += enc.decode(out[i])

    html = ''
    html = add_content(html, header(
        'Input Seed ', color='black', gen_text='Network Output'))
    html = add_content(html, box(seed, text))
    return f'<div>{html}</div>'


def load_gpt2_model():
    """Load in the pre-trained model"""

    # Load Model File
    state_dict = torch.load('../models/gpt2-pytorch_model.bin', map_location='cpu' if not torch.cuda.is_available() else None)

    seed = random.randint(0, 2147483647)
    np.random.seed(seed)
    torch.random.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    global device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load Model
    global config
    config = GPT2Config()
    global model
    model = GPT2LMHeadModel(config)
    model = load_weight(model, state_dict)
    model.to(device)
    model.eval()


# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        # Generate a random sequence
        return render_template('seeded.html', seed=seed, input=text_generator(seed=seed))
    # Send template information to index.html
    return render_template('index.html', form=form)


if __name__ == "__main__":
    print(("* Loading model and Flask starting server..."
           "please wait until server has fully started"))
    load_gpt2_model()
    # Run app
    app.run(host="0.0.0.0", port=5000)
