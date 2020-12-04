#!/usr/bin/env python
# coding: utf-8

# In[670]:

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import keyboard as kb
import sounddevice as sd
import math
import threading


#I) Usuário seleciona o tempo de duração da nota escolhendo a duração do ataque, sustain e release
#II) Usuário escolhe a tensão que alimentará o VCO e a forma de onda desejada
#III) Usuário escolhe a tensão de controle do VCA


# In[671]:


def vco(t, voltage, waveform = "square", max_frequency = 4000, max_input_voltage = 5):
    
    if waveform == 'square':
        return signal.square(2 * np.pi * (max_frequency/max_input_voltage) * voltage * t, 0.5)
    if waveform == 'sawtooth':
        return signal.sawtooth(2 * np.pi * (max_frequency/max_input_voltage) * voltage * t, 1)
    if waveform == 'triangle':
        return signal.sawtooth(2 * np.pi * (max_frequency/max_input_voltage) * voltage * t, 0.5)
    


# In[672]:


def adsr(attack_duration, sustain_duration, release_duration, sustain_height = 5, fs = 44100):
    envelope_duration = attack_duration + sustain_duration + release_duration
    t = np.linspace(0, envelope_duration, math.floor(envelope_duration*fs), endpoint=False)
    attack_sample = secs_to_samples(attack_duration, fs)
    sustain_sample = secs_to_samples(attack_duration + sustain_duration, fs)
    release_sample = secs_to_samples(envelope_duration, fs)
    attack = (sustain_height/attack_duration) * t[0 : attack_sample]
    sustain = sustain_height*np.ones(sustain_sample - attack_sample)
    release = (sustain_height/np.exp((sustain_height/(-release_duration)) * (t[sustain_sample] - envelope_duration)))*np.exp((sustain_height/(-release_duration)) * (t[sustain_sample : ] - envelope_duration))
    return np.concatenate((attack, sustain, release))


# In[673]:


def vca(input_signal, envelope, gain = 5, max_control_voltage = 5):
    return gain/max_control_voltage * envelope * input_signal


# In[674]:


def samples_to_secs(num_samples, fs = 44100):
    return  num_samples/fs

def secs_to_samples(seconds, fs = 44100):
    return math.floor(seconds * fs)


def routine():
    print('Insira a duração do ataque da sua nota:')
    t_a = float(input())
    print('Insira a duração do sustain da sua nota:')
    t_s = float(input())
    print('Insira a duração do release da sua nota:')
    t_r = float(input())

    note_duration = t_a + t_s + t_r
    envelope = adsr(t_a, t_s, t_r)
    t = np.linspace(0, note_duration, secs_to_samples(note_duration, fs), endpoint=False)

    print('Insira tensão de controle do VCO:')
    vco_input = float(input())
    print('Escolha a forma de onda desejada:')
    waveform_input = str(input())
    vco_output = vco(t, vco_input, waveform_input)

    print('Escolha a tensão de controle do VCA:')
    vca_input = float(input())
    vca_output = vca(vco_output, envelope, vca_input)

    print("""
            Pressione "up"/"down" para soar a nota. Uma janela se abrirá em seguida.
            Caso queira soar a nota novamente, feche a janela e aperte "up"/"down".
          """)
    
    while (True):
        if kb.is_pressed('up'):
            plt.plot(t, vca_output)
            sd.play(vca_output, fs)
            plt.show()
        if kb.is_pressed('down'):
            vco_output_feedback = vco(t, envelope, waveform_input)
            vca_output_feedback = vca(vco_output_feedback, envelope, vca_input)
            plt.plot(t, envelope)
            plt.plot(t, vca_output_feedback)
            sd.play(vca_output_feedback, fs)
            plt.show()
        if kb.is_pressed('esc'):
            break
        
def digital_keyboard():
    t_a = 0.05
    t_s = 0.001
    t_r = 0.6
    note_duration = t_a + t_s + t_r
    envelope = adsr(t_a, t_s, t_r)
    t = np.linspace(0, note_duration, secs_to_samples(note_duration, fs), endpoint=False)
    waveform_input = "square"
    print("""
             a = C4
             s = D4
             d = E4
             f = F4
             g = G4
             h = A4
             j = B4
             esc = Sair
          """)
    while (True):
        if kb.is_pressed('a'): #C4
            vco_input = 0.0654
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            #sd.play(vca_output, fs)
            play = threading.Thread(target=sd.play, args=(vca_output, fs))
            play.run()
        if kb.is_pressed('s'): #D4
            vco_input = 0.0734
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)
        if kb.is_pressed('d'): #E4
            vco_input = 0.0824
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)
        if kb.is_pressed('f'): #F4
            vco_input = 0.0873
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)
        if kb.is_pressed('g'): #G4
            vco_input = 0.098
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)
        if kb.is_pressed('h'): #A4
            vco_input = 0.11
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)
        if kb.is_pressed('j'): #B4
            vco_input = 0.124
            vco_output = vco(t, vco_input, waveform_input)
            vca_output = vca(vco_output, envelope)
            sd.play(vca_output, fs)   
        if kb.is_pressed('esc'):
            break

def noise_generator(signal_duration = 1, fs = 44100):
    print("Escolha uma cor de ruído entre: white, pink")
    color = str(input())
    if color == 'white':
        noise = np.random.randn(secs_to_samples(signal_duration, fs))
        while(True):
            if kb.is_pressed('up'):
                sd.play(noise, fs)
            if kb.is_pressed('esc'):
                break
            
    if color == 'pink':
        t = np.linspace(1, signal_duration, secs_to_samples(signal_duration, fs))
        f = np.linspace(1, math.floor(fs/2), math.ceil(fs/2))
        pink_impulse_response = np.fft.ifft(1/f)
        white_noise = np.random.randn(secs_to_samples(signal_duration, fs)) 
        noise = np.real(signal.convolve(white_noise, pink_impulse_response))
        plt.plot(np.linspace(0, 1, fs + math.floor(fs/2) - 1), noise)
        plt.show()
        while(True):
            if kb.is_pressed('up'):
                sd.play(100 * noise, fs)
            if kb.is_pressed('esc'):
                break

# In[717]:
def message():
    print("================================================================================================")
    print(
            """Instruções de uso: \n
            i) A duração da sua nota será determinada pela soma das durações de seu ataque, 
            sustain e release. Insira valores maiores que 0 para todos eles. \n
            ii) As formas de onda disponíveis são: square, triangle e sawtooth. \n
            iii) A tensão máxima de controle de VCO é de 5V e a frequência máxima
            de oscilação é de 4kHz. Para gerar uma frequência f basta calcular (f/4000)
            e inserir a tensão correspondente. \n
            iv) A tensão de controle do VCA tem ganho unitário para 5V. Para ganho arbitrário, 
            basta calcular (tensão/5) e inserir o valor correspondente. \n
            v) O botão de trigger está vinculado à tecla "up" do teclado. Um clique corresponde
            a um, e apenas um, toque completo da nota. Até o momento o sistema é monofônico. \n
            vi) Há a possibilidade de inserir a envoltória gerada como tensão de controle
            do VCO apertando a tecla "down", produzindo um som peculiar. \n
            vii) O modo analógico permite escolher qualquer parâmetro e visualizar a nota gerada,
            mas apenas uma pode ser tocada por programa rodado. Já no modo digital, as teclas
            possuem parâmetros pré-definidos, mas podem ser tocadas como um teclado digital
            monofônico. \n
            viii) Para rodar o programa novamente pressione a tecla "esc" após a seção de áudio. \n
            """)
    print("================================================================================================")


fs = 44100
def main():
    
    message()

    # In[714]:
    while(True):
        print("Digite 0 para sair, 1 para o modo analógico ou 2 para o modo digital e 3 para ruído")
        choice = int(input())
        if choice == 0:
            break
        if choice == 1:
            routine()
        if choice == 2:
            digital_keyboard()
        if choice == 3:
            noise_generator();
            

	# In[715]:


	#plt.plot(t, envelope)
	#plt.plot(t, vco_output)
	#plt.plot(t, vca_output)


# In[676]:


#fs = 44100
#note_length = 1
#t_a = note_length * 1/10
#t_s = note_length * 4/10
#t_r = note_length * 5/10
#note_frequency = 100
#note_duration = t_a + t_s + t_r
#envelope = adsr(t_a, t_s, t_r)
#t = np.linspace(0, note_duration, secs_to_samples(note_duration, fs), endpoint=False)
#vco_output = vco(t, note_frequency/4000, "triangle")
#vca_output = vca(vco_output, envelope)
#vco_output2 = vco(t, note_frequency/2/4000, 'triangle')
#vca_output2 = vca(vco_output2, envelope)
#vco_output3 = vco(t, vco_output)
#vca_output3 = vca(vco_output3, envelope)


# In[679]:


#plt.plot(t, envelope)
#plt.plot(t, vco_output)
#plt.plot(t, vca_output)


# In[693]:


                   


# In[ ]:
if __name__ == '__main__':
    main()
