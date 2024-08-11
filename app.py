from flask import Flask, render_template, request
import pickle

# Setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value[0]  # Ensure only the first prediction value is returned

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    pred = 0
    form_data = {
        'ram': '',
        'weight': '',
        'company': '',
        'typename': '',
        'opsys': '',
        'cpuname': '',
        'gpuname': '',
        'touchscreen': [],
        'ips': []
    }

    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []

        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']

        def traverse(lst, value):
            for item in lst:
                feature_list.append(1 if item == value else 0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)
        
        pred = prediction(feature_list)

        # Update form_data dictionary with the submitted values
        form_data.update({
            'ram': ram,
            'weight': weight,
            'company': company,
            'typename': typename,
            'opsys': opsys,
            'cpuname': cpu,
            'gpuname': gpu,
            'touchscreen': touchscreen,
            'ips': ips
        })

    return render_template('index.html', pred=pred, form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
