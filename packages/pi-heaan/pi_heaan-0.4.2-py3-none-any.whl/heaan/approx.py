
import copy
import heaan
from heaan import (
    HomEvaluator,
    PublicKeyPack,
    Ciphertext
)

def sign(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    n1: int=7,
    n2: int=4
):
    degree = 4
    coeffs = [315, -420, 378, -180, 35]
    coeffs_g = [5850/1024, -34974/1024, 97015/1024, -113492/1024, 46623/1024]
    cost_per_iter = 6

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()
    ctxt_pows = [heaan.Ciphertext() for _ in range(degree+1)]

    ctxt_out = ctxt_in

    # print(id(ctxt_out))
    # if ctxt_in is not ctxt_out:
    #     ctxt_out = copy.deepcopy(ctxt_in)

    conj_key = keypack.get_conj_key()

    for _ in range(n1):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, cost_per_iter)
            
        ctxt_pows[0] = ctxt_out
        eval.mult(ctxt_pows[0], ctxt_pows[0], keypack, ctxt_pows[1])

        for j in range(2, degree+1):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        eval.mult(ctxt_pows[1], coeffs_g[1], ctxt_tmp1)
        for j in range(2, degree+1):
            eval.mult(ctxt_pows[j], coeffs_g[j], ctxt_tmp2)
            eval.add(ctxt_tmp1, ctxt_tmp2, ctxt_tmp1)
        eval.add(ctxt_tmp1, coeffs_g[0], ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_pows[0], keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)

    for _ in range(n2):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, cost_per_iter)
            
        ctxt_pows[0] = ctxt_out
        eval.mult(ctxt_pows[0], ctxt_pows[0], keypack, ctxt_pows[1])

        for j in range(2, degree+1):
            if j%2 == 0:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2], keypack, ctxt_pows[j])
            else:
                eval.mult(ctxt_pows[j//2], ctxt_pows[j//2+1], keypack, ctxt_pows[j])
        
        eval.mult(ctxt_pows[1], coeffs[1], ctxt_tmp1)
        for j in range(2, degree+1):
            eval.mult(ctxt_pows[j], coeffs[j], ctxt_tmp2)
            eval.add(ctxt_tmp1, ctxt_tmp2, ctxt_tmp1)
        eval.add(ctxt_tmp1, coeffs[0], ctxt_tmp1)
        eval.mult(ctxt_tmp1, 1/128, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_pows[0], keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    print("sign finish: ", ctxt_out._data[:5])
    print(id(ctxt_out))
    pass

def inverse(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    n: int=18,
    m: int=20
):
    cost_per_iter = 1

    ctxt_in_neg, ctxt_tmp0, ctxt_tmp1 = heaan.Ciphertext(), heaan.Ciphertext(), heaan.Ciphertext()

    conj_key = keypack.get_conj_key()

    if ctxt_in is not ctxt_out:
        ctxt_out = copy.deepcopy(ctxt_in)
    
    eval.mult(ctxt_in, 1/pow(2, 44), ctxt_tmp0)

    eval.negate(ctxt_in, ctxt_in_neg)
    __check_level_and_bootstrap(eval, keypack, ctxt_in_neg, cost_per_iter)
    
    eval.mult(ctxt_in, 1/pow(2, 22), ctxt_out)
    eval.negate(ctxt_out, ctxt_out)
    eval.add(ctxt_out, 1, ctxt_out)

    for _ in range(m):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, cost_per_iter)        
        eval.mult(ctxt_out, ctxt_out, keypack, ctxt_out)
    
    eval.sub(ctxt_out, ctxt_tmp0, ctxt_out)
    eval.add(ctxt_out, pow(2, -21), ctxt_out)
    
    for _ in range(n):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, cost_per_iter)        
        eval.mult(ctxt_in_neg, ctxt_out, keypack, ctxt_tmp1)
        eval.add(ctxt_tmp1, 2, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_out, keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    pass

def sqrt_inv(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    y0: float=1.6,
    num_iter: int=20
):
    cost_per_iter = 5

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()

    conj_key = keypack.get_conj_key()

    if ctxt_in is not ctxt_out:
        ctxt_out = copy.deepcopy(ctxt_in)

    for i in range(num_iter):
        if i == 0:
            eval.mult(ctxt_in, y0*y0, ctxt_tmp1)
        else:
            if ctxt_out.get_level() - cost_per_iter < ctxt_out.get_min_level_for_bootstrap():
                eval.mult(ctxt_out, 1/32, ctxt_out)
                eval.bootstrap(ctxt_out, keypack, ctxt_out)
                eval.mult(ctxt_out, 1<<5, ctxt_out)
            eval.mult(ctxt_out, ctxt_out, keypack, ctxt_tmp1)
            eval.mult(ctxt_in, ctxt_tmp1, keypack, ctxt_tmp1)
        
        eval.negate(ctxt_tmp1, ctxt_tmp1)
        eval.add(ctxt_tmp1, 3, ctxt_tmp1)
        eval.mult(ctxt_tmp1, 0.5, ctxt_tmp1)

        if i == 0:
            eval.mult(ctxt_tmp1, y0, ctxt_out)
        else:
            eval.mult(ctxt_tmp1, ctxt_out, keypack, ctxt_out)
        eval.kill_imag(ctxt_out, conj_key, ctxt_out)
    pass

def compare(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt1: Ciphertext,
    ctxt2: Ciphertext,
    ctxt_out: Ciphertext,
    n1: int=7,
    n2: int=4
):
    ctxt_tmp = heaan.Ciphertext()
    eval.sub(ctxt1, ctxt2, ctxt_tmp)
    sign(eval, keypack, ctxt_tmp, ctxt_out, n1, n2)
    eval.add(ctxt_out, 1, ctxt_out)
    eval.mult(ctxt_out, 0.5, ctxt_out)
    pass

def sqrt(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt_in: Ciphertext,
    ctxt_out: Ciphertext,
    num_iter: int=20
):
    cost_per_iter = 2

    ctxt_tmp1, ctxt_tmp2 = heaan.Ciphertext(), heaan.Ciphertext()

    if ctxt_in is not ctxt_out:
        ctxt_out = copy.deepcopy(ctxt_in)

    eval.sub(ctxt_in, 1, ctxt_tmp)

    for _ in range(num_iter):
        __check_level_and_bootstrap(eval, keypack, ctxt_out, cost_per_iter)
        __check_level_and_bootstrap(eval, keypack, ctxt_tmp, cost_per_iter)

        eval.mult(ctxt_tmp1, 0.5, ctxt_tmp2)
        eval.negate(ctxt_tmp2, ctxt_tmp2)
        eval.add(ctxt_tmp2, 1, ctxt_tmp2)
        eval.mult(ctxt_out, ctxt_tmp2, keypack, ctxt_out)

        eval.sub(ctxt_tmp1, 3, ctxt_tmp2)
        eval.mult(ctxt_tmp2, 0.25, ctxt_tmp2)
        eval.mult(ctxt_tmp1, ctxt_tmp1, keypack, ctxt_tmp1)
        eval.mult(ctxt_tmp1, ctxt_tmp2, keypack, ctxt_tmp1)
    pass

def __check_level_and_bootstrap(eval: HomEvaluator,
    keypack: PublicKeyPack,
    ctxt: Ciphertext,
    cost_per_iter: int
):
    if ctxt.get_level() - cost_per_iter < ctxt.get_min_level_for_bootstrap():
        eval.bootstrap(ctxt, keypack, ctxt)
    pass
