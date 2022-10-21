import time
from tools import sat, deadzone

class MotorControl:
    def __init__(self, refk, kp, ki, deadzone):
        self.kp = kp
        self.ki = ki
        self.refk = refk
        self.deadzone = deadzone
        self.old_err = 0
        self.old_out = 0
        
        self.int = 0
        self.last_time = -1
        
    def actuate(self, ref, err):
        now = time.time()
        dt = now - self.last_time if self.last_time > 0 else 0.040
        
        self.int = sat(self.int + err * dt, 64)
        out = self.refk * ref + self.kp * err + self.ki * self.int
        
        
        return int(deadzone(sat(out, 255), self.deadzone, -self.deadzone))

    def actuatePaper(self, ref, err):
        ki = self.ki
        kp = self.kp
        T = 0.03
        # now = time.time()
        # T = now - self.last_time if self.last_time > 0 else 0.040
        
        c0 = -kp + T/2 * ki
        c1 = kp + T/2 * ki
        A = 1 / T
        
        out = self.old_out + A * (c1 * err + c0 * self.old_err)
        self.old_err = err
        self.old_out = out if abs(out) <= 127 else 0

        return int(deadzone(sat(out, 255), self.deadzone, -self.deadzone))

    #     double PImotorA(double err){
    #     static double old_err;
    #     static double old_out;
    #     double out = (  1.6 * (err - 0.91  *  old_err) + old_out);
    #     old_err = err; //- (saturation(out)-out);
    #     //  1.6 * (1-0.91 * z^-1)/(1-z^-1)
    #     //  1.6 * (z-0.91)/(z-1)    Projetado a partir do LGR pro motor (identificação o motor)
    #     //
    #     // 1 - Identificar novo motor (com carga/com roda e no chão)
    #     //                              -MATLAB identificação de sistemas
    #     //                              -sintonização de constantes
    #     // 2 - Projetar um controlador (contínuo)
    #     // 3 - Discretizar controlador (mapeamento direto com transformada z)
    #     //                              -comando MATLAB: c2d(tf,T,"matched")
    #     // 4 - Expandir função de transferencia e isolar U(z)
    #     // 5 - Transformada inversa de z
    #     //
    #     //  z = e^(sT)

    #     old_out = (abs(out) < 255)? out : 0;    // anti-windup (evita que o erro de saturação seja considerado como erro)
    #     return out;
    # }
