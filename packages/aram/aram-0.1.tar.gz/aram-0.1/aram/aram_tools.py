import numpy as np
import numpy.linalg as la
import scipy as sp
#import healpy as hp
import time
from IPython.display import display,clear_output

gaussian_beam = lambda z, w0, l, n : np.sqrt(1/np.square(z) + np.square(l) / np.square(w0 * np.pi * n))

class progress_bar():
    
    def __init__(self,n_total,n_width=16,n_per=1,task=''):
        self.n_total = n_total
        self.n_width = n_width
        self.t_start = time.time()
        self.mtpl    = 0
        self.elapsed = 0
        self.eta     = 0
        self.output  = ''
        self.n_per   = n_per
        self.totlen  = len(f'{self.n_total}')
        self.task    = task
        
    def update(self,n_done):
        if (n_done % self.n_per == 0) or (n_done == self.n_total):
            raw_elapsed  = time.time() - self.t_start
            self.mtpl    = raw_elapsed / n_done  
            raw_eta      = (self.n_total - n_done) * self.mtpl  
            self.elapsed = f'{int(raw_elapsed/60):>02.00f}:{int(raw_elapsed%60):>02.00f}'
            self.eta     = f'{int(raw_eta/60):>02.00f}:{int(raw_eta%60):>02.00f}'
            prp = n_done / self.n_total
            n_f = int(np.floor(self.n_width*prp))
            n_p = self.n_width*prp - n_f
            sym = '' if prp == 1 else [' ','░','▒','▓','█'][int(np.floor(5*n_p))]
            self.pct = f' {100*prp:>5.01f}%'
            donlen = len(f'{n_done}')
            self.output = self.task + self.pct + ' |' + n_f*'█' + sym + np.maximum(self.n_width-n_f-1,0)*' '+ '| ' + (self.totlen-donlen)*' ' \
            + f'{n_done}/{self.n_total}' + f' [{self.elapsed}s<{self.eta}s, {1/self.mtpl:.00f} it/s] '
            print(self.output); clear_output(wait=True)
    
#prog = progress_bar(n_total=5000,n_per=16,task='testing...')
#for i in range(5000):
#    time.sleep(0.001)
#    prog.update(i+1)

def sim_cmb(ra_min, ra_max, dec_min, dec_max, fwhm=0, d_ra=1/60, d_dec=1/60, nside=2048, kind='TT'):
    
    ra_bins  = np.arange(ra_min, ra_max + d_ra, d_ra)
    dec_bins = np.arange(dec_min, dec_max + d_dec, d_dec)
    ra_mids  = ra_bins[1:]/2 + ra_bins[:-1]/2
    dec_mids = dec_bins[1:]/2 + dec_bins[:-1]/2
    RA, DEC  = np.meshgrid(ra_mids, dec_mids)
    
    cmb_ps = np.load('products/cmb_spectra/act+wmap.npy')
    if kind=='TT':
        ll_C_l = cmb_ps[1]
    if kind=='EE':
        ll_C_l = cmb_ps[2]
        
    alm      = hp.synalm(ll_C_l / (cmb_ps[0] * (cmb_ps[0] + 1)), new=True)    
    sub_cmb  = hp.alm2map(alm,nside, fwhmfloat=fwhm, pol=True)[hp.pixelfunc.ang2pix(nside=nside, theta=RA, phi=DEC, nest=False, lonlat=True)]
    bcmb     = sp.stats.binned_statistic_2d(RA.ravel(),DEC.ravel(),sub_cmb.ravel(),bins=[ra_bins,dec_bins],statistic='mean')[0].T[::-1]
    return RA, DEC, bcmb

#RA,DEC,cmb = sim_cmb(30,40,30,40,kind='TT')



def make_array(array_shape,max_fov,max_n_det):
    if array_shape=='phyllotaxis':
        phi = np.pi*(3.-np.sqrt(5.))  # golden angle in radians
        dzs = np.zeros(max_n_det).astype(complex)
        for i in range(max_n_det):
            dzs[i] = np.sqrt((i / (max_n_det - 1)) * 2 ) *np.exp(1j*phi*i)
        od = np.abs(np.subtract.outer(dzs,dzs))
        dzs *= max_fov / od.max()
    if array_shape=='hex':
        HEX  = lambda n : 3*n*(n+1) + 1 ; hex_layers = 0
        while HEX(hex_layers+1) < max_n_det: hex_layers += 1 
        dr   = max_fov/ (2 * hex_layers)
        dzs  = np.zeros(1).astype(complex)
        angs = np.arange(0,2*np.pi,np.pi/3)+ np.pi/6
        for ilay in range(hex_layers):
            for iz,z in enumerate(dzs):
                for iang,ang in enumerate(angs):
                    z_ = np.round(z+dr*np.exp(1j*ang),6)
                    if np.amin(np.abs(z_-dzs) > dr/4):
                        dzs = np.append(dzs,z_)
    if array_shape=='square':
        dxy_ = np.linspace(-max_fov,max_fov,int(np.floor(np.sqrt(max_n_det))))/(2*np.sqrt(2))
        DX, DY = np.meshgrid(dxy_,dxy_)
        return DX.ravel(), DY.ravel()
        
    return np.real(dzs), np.imag(dzs)

def make_covariance_matrix(C,x0,y0,z0,x1=None,y1=None,z1=None,auto=True):
    if auto:
        n = len(x0); i,j = np.triu_indices(n,1)
        o = C(np.sqrt(np.square(x0[i] - x0[j]) + np.square(y0[i] - y0[j]) + np.square(z0[i] - z0[j])))
        c = np.empty((n,n)) 
        c[i,j],c[j,i] = o,o
        c[np.eye(n).astype(bool)] = C(0)
    if not auto:
        n = len(x0); i,j = np.triu_indices(n,1)
        c = C(np.sqrt(np.square(np.subtract.outer(x0,x1))
                    + np.square(np.subtract.outer(y0,y1))
                    + np.square(np.subtract.outer(z0,z1))))
    return c


msqrt = lambda M : [np.matmul(u,np.diag(np.sqrt(s))) for u,s,vh in [la.svd(M)]][0]

# 'C' is the normalized covariance function
matern = lambda r,r0,nu : 2**(1-nu)/sp.special.gamma(nu)*sp.special.kv(nu,r/r0+1e-10)*(r/r0+1e-10)**nu
    
def ae_to_xy(az, el, c_az, c_el):
    ground_X, ground_Y, ground_Z = np.sin(az-c_az)*np.cos(el), np.cos(az-c_az)*np.cos(el), np.sin(el)
    az_rot_XY = (ground_X+1j*ground_Y)*np.exp(1j*c_az)
    dx, az_rot_Y = np.real(az_rot_XY), np.imag(az_rot_XY)
    return np.real(az_rot_XY), -np.real((np.imag(az_rot_XY)+1j*ground_Z)*np.exp(1j*c_el))

def xy_to_ae(dx, dy, c_az, c_el):
    el_rot_YZ = (-dy+1j*np.cos(np.sqrt(dx**2+dy**2)))*np.exp(-1j*(np.pi/2-c_el))
    el_rot_Y, ground_Z = np.real(el_rot_YZ),np.imag(el_rot_YZ)
    return np.arctan2(dx,el_rot_Y) + c_az, np.arcsin(ground_Z)

def ae_to_rd(az, el, lst, lat):
    NP_X, NP_Y, NP_Z = np.sin(az)*np.cos(el), np.cos(az)*np.cos(el), np.sin(el)
    lat_rot_YZ = (NP_Y + 1j*NP_Z)*np.exp(1j*(np.pi/2-lat))
    lat_rot_Y, globe_Z = np.real(lat_rot_YZ), np.imag(lat_rot_YZ)
    return np.arctan2(NP_X,-lat_rot_Y) + lst, np.arcsin(globe_Z)
    
def rd_to_ae(ra, de, lst, lat):
    NP_X, globe_Y, globe_Z = np.sin(ra-lst)*np.cos(de), -np.cos(ra-lst)*np.cos(de), np.sin(de)
    lat_rot_YZ = (globe_Y + 1j*globe_Z)*np.exp(-1j*(np.pi/2-lat))
    NP_Y, NP_Z = np.real(lat_rot_YZ), np.imag(lat_rot_YZ)
    return np.arctan2(NP_X,NP_Y), np.arcsin(NP_Z)