import sys
import time
import pickle
import scipy as sp
import numpy as np
import numpy.linalg as la
from scipy import signal, stats
import ephem
from datetime import datetime
from datetime import timezone
from IPython.display import display,clear_output
#import healpy
from aram import aram_tools
from aram import resources
import gc
import os

import pkg_resources



# an array object describes the array of detectors. all of the arguments are dimensionful arrays of the same length 

class array():
    def __init__(self, array_config=None, fov_tol=2e-2, verbose=True):
        
        default_array_config = {'array_shape' : 'hex',
                                'n_detectors' : 600,      # maximum number of detectors
                                  'array_fov' : 5,        # maximum span of array
                                       'fwhm' : 5 / 60,   # in degrees
                                       'band' : 1.5e11,   # observing band (in Hz)
                                       'pink' : 4e-1,     # pink noise scaling 
                                      'white' : 1e0}      # white noise scaling 
        
        # use default config if none supplied
        if array_config==None:
            print('No array config specified, using default array.')
            array_config = default_array_config
            
        # have the offsets been put in manually?
        manual_offsets = np.all(np.isin(['offset_x','offset_y'],list(array_config)))
        
        # fill missing arguments with the defaults
        for arg in list(default_array_config):
            if not arg in list(array_config):
                array_config[arg] = default_array_config[arg]
                
        # make the array offsets, if necessary        
        if not manual_offsets:
            array_config['offset_x'], array_config['offset_y'] = aram_tools.make_array(array_config['array_shape'], 
                                                                                       array_config['array_fov'], 
                                                                                       array_config['n_detectors']) 
        self.z = np.radians(array_config['offset_x']) + 1j*np.radians(array_config['offset_y'])
        self.z -= self.z.mean()
        self.x = np.real(self.z)
        self.y = np.imag(self.z)
        self.n = len(self.z)
        
        for arg in list(['fwhm','band','pink','white']):
            if not isinstance(array_config[arg],np.ndarray):
                array_config[arg] = array_config[arg] * np.ones(self.n)
                       
        self.fwhm  = np.radians(array_config['fwhm'])
        self.band  = array_config['band']
        self.pink  = array_config['pink']
        self.white = array_config['white']
        self.fov_r = (1 + fov_tol) * (np.abs(self.z).max()) + self.fwhm.max() 
            
#arr = array(array_config)


class site():
    def __init__(self, site_config=None):
        
        with open(pkg_resources.resource_filename('aram', 'resources/sites/site_dict'), 'rb') as f:
            self.site_dict = pickle.load(f)

        site_list = '\nsite' + 5*' ' + 'location' + 4*' ' + 'longitude' + 2*' ' + 'latitude' + 2*' ' + 'height'
        site_list += '\n' + (len(site_list)-1)*'-'
        for sitename in list(self.site_dict):
            name,loc,lon,lat,hgt = [self.site_dict[sitename][key] for key in ['longname','location','longitude','latitude','altitude']]
            lon_name = f'{np.round(np.abs(lon),3):>8}°' + ['W','E'][int(lon>0)]
            lat_name = f'{np.round(np.abs(lat),3):>7}°' + ['S','N'][int(lon>0)]
            site_list += f'\n{sitename:<8} {loc:<10} {lon_name} {lat_name} {hgt:>6.0f}m'

        self.site = ephem.Observer()
        default_site_config = {'site' : 'ACT',
                               'time' : datetime.now(timezone.utc).timestamp()}
                
        if site_config==None:
            print('No site config specified, using the ACT site.')
            site_config = default_site_config
            
        manual_site = np.all(np.isin(['location','latitude','longitude','altitude'],list(site_config)))
        
        for arg in ['site','time']:
            if not arg in list(site_config):
                site_config[arg] = default_site_config[arg]
        if manual_site: 
            location, latitude, longitude, altitude = site_info['location'], site_config['latitude'], site_config['longitude'], site_config['altitude']
        else:
            if not site_config['site'] in list(self.site_dict):
                raise Exception(f'Not a supported site. Available sites are:\n' + site_list)
            else:
                site_info = self.site_dict[site_config['site']]
                self.is_auto = True
                location, latitude, longitude, altitude = site_info['location'], site_info['latitude'], site_info['longitude'], site_info['altitude']

        #print(latitude, longitude, altitude)
        self.location = location
        self.site.lat, self.site.lon, self.site.elevation = str(latitude), str(longitude), altitude
        self.timestamp = site_config['time']
        
        self.site.date = datetime.fromtimestamp(self.timestamp)
        
        if self.is_auto:
            self.yday = datetime.fromtimestamp(self.timestamp).timetuple().tm_yday - 1
            self.hour = datetime.fromtimestamp(self.timestamp).timetuple().tm_hour - 1

            self.ihour = int(self.hour/3) if self.hour < 22.5 else 0
            self.iyday = int(self.hour/7) 

            with open(pkg_resources.resource_filename('aram', 'resources/weather/norm_gen'), 'rb') as handle:
                norm_gen = pickle.load(handle)
            with open(pkg_resources.resource_filename('aram', 'resources/weather/mode_avg'), 'rb') as handle:
                mode_avg = pickle.load(handle)
            with open(pkg_resources.resource_filename('aram', 'resources/weather/mode_rms'), 'rb') as handle:
                mode_rms = pickle.load(handle)

            gw = np.matmul(norm_gen[self.location][self.iyday,self.ihour],np.random.standard_normal(16)).reshape((4,33))
            self.gw_dict = {}
            for icol,col in enumerate(['LQV','T','U','V']):
                gw[icol] *= mode_rms[self.location][col]
                gw[icol] += mode_avg[self.location][col]
                self.gw_dict[col] = gw[icol]
            self.gw_dict['QV'] = np.exp(self.gw_dict['LQV'])
        
class observation():
    def __init__(self, site_config=None, obs_config=None):
        
        default_obs_config = {'duration'  : 600,'samp_freq' : 20,
                              'center_az' : 0, 'center_el'  : 90, 'az_throw' : 0, 'az_speed' : 0}

        if obs_config==None:
            print('No obs config specified, defaulting to a 10-minute zenith stare at 20 Hz.')
            obs_config = default_obs_config
            
        for arg in list(default_obs_config):
            if not arg in list(obs_config):
                obs_config[arg] = default_obs_config[arg]
            
        self.duration = obs_config['duration']
        self.dt    = 1/obs_config['samp_freq']
        self.t_    = np.arange(0,self.duration,self.dt); self.T = len(self.t_); self.f_ = np.fft.fftfreq(self.T,self.dt)
        self.c_az, self.c_el = np.radians(obs_config['center_az']), np.radians(obs_config['center_el'])
        self.r_az, self.v_az = np.radians(obs_config['az_throw']),  np.radians(obs_config['az_speed'])
        self.c_az_ = self.c_az + self.r_az*sp.signal.sawtooth(np.pi/2 + 2*np.pi*self.v_az*(self.t_-self.t_.min())/(4*self.r_az+1e-16),width=.5)
        self.c_el_ = self.c_el + np.zeros(self.T)

class model():
    
    def __init__(self,array_config=None, site_config=None, obs_config=None, model_config=None, other_config=None, full_compute=False, verbose=False):
        
        default_model_config = {'n_layers'     : 4,
                                'min_height'   : 1000,
                                'max_height'   : 3000,
                                'sig_res'      : 1,
                                'half_height'  : 1500,
                                'atm_rms'      : 50,  
                                'wind_speed'   : 50,
                                'wind_bearing' : 0,
                                'cov_type'     : 'matern',
                                'outer_scale'  : 500,
                                'power_law'    : -8/3}  
        
        default_other_config = {'fov_tol' : 5e-2, 'n_dz_samp' : 16, 'n_ca_samp' : 16, 'n_st_samp' : 16, 'n_sam_max' : 10000}
        
        # MODEL CONFIGURATION
        if model_config==None:
            self.model_is_default = True  
            print('No model config specified, using default atmospheric model.')
            model_config = default_model_config
            
        if other_config==None:
            self.other_is_default = True  
            other_config = default_other_config
            
        self.array = array(array_config=array_config)
        self.site  = site(site_config=site_config)
        self.obs   = observation(obs_config=obs_config)
        
        self.default_interp_method = 'rectilinear' if np.sum(self.array.fwhm[0]==self.array.fwhm)==self.array.n else 'brute_gaussian'

        self.obs.mlst0 = float(self.site.site.sidereal_time()) 
        self.obs.mlst_ = self.obs.mlst0 % (2*np.pi) + ((2*np.pi / 86400) * self.obs.t_) % (2*np.pi) # mean local sidereal time        
        self.ca_samp = self.obs.c_az + np.linspace(-self.obs.r_az,self.obs.r_az,other_config['n_ca_samp'])#+ np.pi/2
        self.dz_samp = self.array.fov_r * np.exp(1j*np.linspace(0,2*np.pi,other_config['n_dz_samp']+1)[:-1])
        self.st_samp = np.linspace(self.obs.mlst_[0],self.obs.mlst_[-1],other_config['n_st_samp'])
        self.dx_samp, self.dy_samp = np.real(self.dz_samp), np.imag(self.dz_samp)
        self.fov_simp = sp.spatial.Delaunay(np.vstack([self.dx_samp, self.dy_samp]).T, incremental=False, qhull_options=None)

        DZ_SAMP, ST_SAMP, CA_SAMP = np.meshgrid(self.dz_samp, self.st_samp, self.ca_samp)
        DX_SAMP, DY_SAMP = np.real(DZ_SAMP), np.imag(DZ_SAMP)
        AZ_SAMP, EL_SAMP = aram_tools.xy_to_ae(DX_SAMP, DY_SAMP, CA_SAMP, self.obs.c_el)
        RA_SAMP, DE_SAMP = aram_tools.ae_to_rd(AZ_SAMP, EL_SAMP, ST_SAMP, self.site.site.lat)

        self.sp_dx,self.sp_dy  = DX_SAMP[0], DY_SAMP[0]
        self.sp_a,self.sp_e    = AZ_SAMP[0], EL_SAMP[0]
        self.rel_z             = np.exp(1j*(np.pi/2-AZ_SAMP[0])) / np.tan(EL_SAMP[0])
        self.rel_x,self.rel_y  = np.real(self.rel_z),np.imag(self.rel_z)
        self.sp_ra,self.sp_dec = RA_SAMP, DE_SAMP
        
        #self.az_, self.el_  = aram_tools.xy_to_ae(self.array.x[:,None],self.array.y[:,None],self.c_az_[None,:],self.c_el_[None,:])
        #self.ra_, self.dec_ = aram_tools.ae_to_rd(self.az_, self.el_,self.mlst_[None,:],self.site.lat)
        
        auto_heights   = np.all(np.isin(['min_height','max_height','n_layers'],list(model_config)))
        manual_heights = np.all(np.isin(['heights'],list(model_config)))
        if auto_heights:  
            self.heights = np.linspace(model_config['min_height'], model_config['max_height'], model_config['n_layers'])
        if manual_heights:  
            if isinstance(model_config['heights'], np.ndarray):
                self.heights = model_config['heights']
            else:
                raise Exception('\'heights\' parameter must be a numpy array.')
        if not (auto_heights or manual_heights):
            raise Exception('Could not build atmospheric layers. Please specify the \'min_height\', \'max_height\', and \'n_layers\' parameters, or else enter an array of heights.')
        
        for arg in list(default_model_config):
            if not arg in list(model_config):
                model_config[arg] = default_model_config[arg]
            thing = model_config[arg]
            exec(f'self.{arg} = thing')
                
        self.n_layers = len(self.heights)
        
        if self.site.is_auto:
            self.weather = {}
            for col in ['QV','T','U','V']:
                self.weather[col] = np.interp(self.heights,np.arange(0,6600,200),self.site.gw_dict[col]) 
            z = self.weather['V'] + 1j*self.weather['U']
            self.weather['ws'], self.weather['wa'] = np.abs(z), np.angle(z)
            self.wind_bearing = self.weather['wa']
            self.wind_speed = self.weather['ws']
        
        else:
                
            if isinstance(model_config['wind_speed'], np.ndarray):
                self.wind_speed = model_config['wind_speed']
            else:
                self.wind_speed = model_config['wind_speed'] * np.ones(self.n_layers)

            if isinstance(model_config['wind_bearing'], np.ndarray):
                self.wind_bearing = np.radians(model_config['wind_bearing'])
            else:
                self.wind_bearing = np.radians(model_config['wind_bearing']) * np.ones(self.n_layers)

            if not (len(self.wind_speed) == self.n_layers and len(self.wind_bearing) == self.n_layers):
                raise Exception('Shape mismatch in the heights and the wind velocities.')

        if model_config['cov_type'] == 'matern':
            self.r0, self.nu = model_config['outer_scale'], (-1-model_config['power_law'])/2
            self.C = lambda r: 2**(1-self.nu)/sp.special.gamma(self.nu)*sp.special.kv(self.nu,r/self.r0+1e-10)*(r/self.r0+1e-10)**self.nu
        
        self.array.wavelength = 2.998e8 / self.array.band
                
        self.depths   = self.heights / np.sin(self.obs.c_el)
        self.ff_sig   = self.array.fwhm / (2*np.sqrt(2*np.log(2)))
        self.w0       = self.array.wavelength / (self.ff_sig * np.pi * 1.003)
        self.ang_sig_ = aram_tools.gaussian_beam(self.depths[None,:],self.w0[:,None],l=self.array.wavelength[:,None],n=1.003)
        self.phy_sig_ = self.ang_sig_.min(axis=0) * self.depths
        
        self.atm_res_ = self.phy_sig_ * model_config['sig_res'] * (2*np.sqrt(2*np.log(2)))
        self.d_orth_  = self.atm_res_ 
        self.d_para_  = self.atm_res_ 
        self.sim_dt_  = self.atm_res_ / self.wind_speed
        
        # time and angle fields for the simulation
        self.sim_t_    = [self.obs.t_[0] + np.arange(-dt,self.obs.duration+dt, dt) for dt in self.sim_dt_]
        self.sim_mlst_ = np.interp(self.sim_t_[0],self.obs.t_,self.obs.mlst_)
        self.sim_T_    = [len(sim_t_) for sim_t_ in self.sim_t_]; self.sim_f_ = [np.fft.fftfreq(T,dt) for T,dt in zip(self.sim_T_,self.sim_dt_)]
        self.tot_sim_T = np.sum(self.sim_T_)
        self.sim_c_az_ = [np.interp(t_,self.obs.t_,self.obs.c_az_) for t_ in self.sim_t_]
        self.sim_c_el_ = [np.interp(t_,self.obs.t_,self.obs.c_el_) for t_ in self.sim_t_]

        self.sim_az_, self.sim_el_ = list(zip(*[aram_tools.xy_to_ae(self.array.x[:,None],self.array.y[:,None],caz[None,:],cel[None,:]) for caz,cel in zip(self.sim_c_az_,self.sim_c_el_)]))
        #self.sim_az_, self.sim_el_ = list(zip(*[aram_tools.xy_to_ae(self.array.x[:,None],self.array.y[:,None],caz[None,:],cel[None,:]) for caz,cel in zip(self.sim_c_az_,self.sim_c_el_)]))
        #
        #self.sim_ra_, self.sim_dec_ = aram_tools.ae_to_rd(self.sim_az_, self.sim_el_,self.sim_mlst_[None,:],self.site.site.lat)
        #self.fov_az_, self.fov_el_  = [aram_tools.xy_to_ae(dx[:,None],dy[:,None],caz[None,:],cel[None,:]) for dx,dy,caz,cel in zip(self.dx_samp,self.dy_samp,self.sim_c_az_,self.sim_c_el_)]
        self.fov_az_, self.fov_el_  = aram_tools.xy_to_ae(self.dx_samp[:,None],self.dy_samp[:,None],self.sim_c_az_[0][None,:],self.sim_c_el_[0][None,:])    
        self.sim_min_az_, self.sim_max_az_ = self.fov_az_.min(axis=0), self.fov_az_.max(axis=0)
        self.sim_min_el_, self.sim_max_el_ = self.fov_el_.min(axis=0), self.fov_el_.max(axis=0)
        
        del self.fov_az_, self.fov_el_
        gc.collect()
        self.lay_z_, self.lay_h_ = [], []
        self.gen_z_, self.gen_h_ = [], []
        self.n_para_, self.n_orth_ = [], []
        self.lay_para_, self.lay_orth_ = [], []
        self.sam_i_ = []
        
        # this is messy, but necessary
        if verbose:
            print('  # | height [m] | res. [m] | n_para | n_ortho |  n_total | n_sam | n_gen ')

        self.good_layer_ = np.ones(self.n_layers).astype(bool)
        
        for i_h,h in enumerate(self.heights):
            
            adj_bear = 3*np.pi/2 + self.wind_bearing[i_h]
            self.rot_ch_z    = h * self.rel_z * np.exp(1j*adj_bear)
            ch_para, ch_orth = np.real(self.rot_ch_z),np.imag(self.rot_ch_z)
            self.lay_para_.append(np.arange(ch_para.min(),ch_para.max()+self.d_para_[i_h], self.d_para_[i_h]))
            self.lay_orth_.append(np.arange(ch_orth.min(),ch_orth.max()+self.d_orth_[i_h], self.d_orth_[i_h]))
            ORTH_G, PARA_G = np.meshgrid(self.lay_orth_[-1],self.lay_para_[-1])
            n_para, n_orth = len(self.lay_para_[-1]), len(self.lay_orth_[-1])
            self.n_para_.append(n_para)
            self.n_orth_.append(n_orth)
            z_ = PARA_G + 1j*ORTH_G
            self.lay_z_.append(z_*np.exp(-1j*adj_bear))
            self.lay_h_.append(h*np.ones(z_.shape))
            self.gen_z_.append((z_[0]-self.d_para_[i_h])*np.exp(-1j*adj_bear))
            self.gen_h_.append(h*np.ones(z_[0].shape))
            i_para_, i_orth_ = [],[]
            for i_para in np.append(0,2**np.arange(np.ceil(np.log(n_para)/np.log(2)))):
                i_orth_.append(np.unique(np.linspace(0,n_orth-1,int(np.maximum(n_orth/(i_para+1),16))).astype(int)))
                i_para_.append(np.repeat(i_para,len(i_orth_[-1])).astype(int))
            i_max  = np.maximum(0,np.max(i_para_[-1])) 
            self.sam_i_.append((np.concatenate(i_para_),np.concatenate(i_orth_)))
            n_    = len(z_.ravel())
            n_sam = len(self.sam_i_[-1][0].ravel())
            n_gen = len(self.gen_z_[-1].ravel())
            
            if n_sam > other_config['n_sam_max']:
                self.good_layer_[i_h] = False
            
            if verbose:
                if self.good_layer_[i_h]:
                    print(f' {i_h:>2} | {h:>10.02f} | {self.atm_res_[i_h]:>8.02f} | {z_.shape[0]:>6.0f} | {z_.shape[1]:>7.0f} | {n_:>7.02e} | {n_sam:>5.0f} | {n_gen:>5.0f}')
                else:
                    print(f' {i_h:>2} | {h:>10.02f} | WARNING: LAYER EXCLUDED')

            
        if (not self.default_interp_method == 'rectilinear') or full_compute:
            
            print('building trees...')
            
            self.sim_dx_, self.sim_dy_  = list(zip(*[aram_tools.ae_to_xy(az,el,caz,cel) for az,el,caz,cel in zip(self.sim_az_, self.sim_el_, self.obs.c_az, self.obs.c_el)]))
            self.lay_x_, self.lay_y_ = [np.real(z)  for z in self.lay_z_], [np.imag(z) for z in self.lay_z_]
            self.lay_a_, self.lay_e_ = [np.pi/2 - np.angle(z) for z in self.lay_z_], [np.pi/2 - np.arctan(np.abs(z/h)) for z,h in zip(self.lay_z_,self.heights)]
            self.lay_dx_, self.lay_dy_, self.lay_dz_ = [], [], []
            for laz,lel in zip(self.lay_a_, self.lay_e_):
                x,y = aram_tools.ae_to_xy(laz,lel,self.obs.c_az,self.obs.c_el)
                self.lay_dx_.append(x), self.lay_dy_.append(y), self.lay_dz_.append(x + 1j*y)

            self.static_ckdt = [sp.spatial.cKDTree(np.vstack([x.ravel(),y.ravel()]).T) for x,y in zip(self.lay_dx_, self.lay_dy_)]

        # this is too 
        if verbose:
            print('computing transition matrices...')
        sam_args = [np.c_[np.real(lz[si]),np.imag(lz[si]),lh[si]] for lz,lh,si in zip(self.lay_z_,self.lay_h_,self.sam_i_)]
        gen_args = [np.c_[np.real(gz),np.imag(gz),gh]             for gz,gh    in zip(self.gen_z_,self.gen_h_)]
        lay_v_   = [np.zeros(lz.shape) for lz in self.lay_z_]
        self.prec_ = [la.inv(aram_tools.make_covariance_matrix(self.C,np.real(lz[si]),np.imag(lz[si]),lh[si])) for lz,lh,si in zip(self.lay_z_,self.lay_h_,self.sam_i_)]
        self.csam_ = [aram_tools.make_covariance_matrix(self.C,np.real(gz),np.imag(gz),gh,np.real(lz[si]),np.imag(lz[si]),lh[si],auto=False) 
                 for lz,lh,si,gz,gh in zip(self.lay_z_,self.lay_h_,self.sam_i_,self.gen_z_,self.gen_h_)]
        self.cgen_ = [aram_tools.make_covariance_matrix(self.C,np.real(gz),np.imag(gz),gh) for gz,gh in zip(self.gen_z_,self.gen_h_)]
        self.A_ = [np.matmul(csam,prec) for prec,csam in zip(self.prec_,self.csam_)]
        self.B_ = [aram_tools.msqrt(cgen-np.matmul(A,csam.T)) for A,cgen,csam in zip(self.A_,self.cgen_,self.csam_)]
        
        print(f'done! total atmospheric points : {n_}')
        
    def atmosphere_timestep(self,i_layer):
        
        self.lay_v_[i_layer] = np.r_[(np.matmul(self.A_[i_layer],self.lay_v_[i_layer][self.sam_i_[i_layer]])
                                 + np.matmul(self.B_[i_layer],np.random.standard_normal(self.B_[i_layer].shape[0])))[None,:],self.lay_v_[i_layer][:-1]]

    def generate_atmosphere(self,blurred=True):

        self.lay_v_ = [np.zeros(lz.shape) for lz in self.lay_z_]
        n_init_ = [si[0].max() for si in self.sam_i_]
        n_ts_   = [T+n_para for T,n_para in zip(self.sim_T_,self.n_para_)]
        tot_n_init, tot_n_ts = np.sum(n_init_), np.sum(n_ts_)
        self.gen_data = [np.zeros((n_ts,v.shape[1])) for n_ts,v in zip(n_ts_,self.lay_v_)]
        
        prog = aram_tools.progress_bar(n_total=tot_n_init,n_per=64,task='INITIALIZING...')
        tot_i_init = 0
        for i_layer, n_init in enumerate(n_init_):
            for i_init in range(n_init):
                prog.update(tot_i_init+1); tot_i_init += 1
                self.atmosphere_timestep(i_layer)
            
        prog = aram_tools.progress_bar(n_total=tot_n_ts,n_per=64,task='GENERATING...')
        tot_i_ts = 0
        for i_layer,n_ts in enumerate(n_ts_):
            for i_ts in range(n_ts):
                prog.update(tot_i_ts+1); tot_i_ts += 1
                self.atmosphere_timestep(i_layer)
                self.gen_data[i_layer][i_ts] = self.lay_v_[i_layer][0]

        if blurred:
            for i_h, h in enumerate(self.heights):
                self.gen_data[i_h] = sp.ndimage.gaussian_filter1d(self.gen_data[i_h],axis=0,sigma=self.phy_sig_[i_h] / self.d_orth_[i_h])
                self.gen_data[i_h] = sp.ndimage.gaussian_filter1d(self.gen_data[i_h],axis=1,sigma=self.phy_sig_[i_h] / self.d_para_[i_h])

    def simulate(self, do_atmosphere=False, 
                       do_cmb=False, 
                       do_noise=False,
                       return_separate=False,
                       interp_method=None, 
                       sky_per_det=16):
        
        if interp_method == None:
            interp_method = self.default_interp_method
        
        #print(f'using {interp_method} interpolation')
        gaussian = lambda offset, sig : np.exp(-.5*np.square(offset/sig))
        
        if do_atmosphere:
            h_atm_sim_data = [np.zeros((self.array.n,sim_T)) for sim_T in self.sim_T_]
            if interp_method=='rectilinear':
                
                self.generate_atmosphere(blurred=True)
                prog = aram_tools.progress_bar(n_total=self.tot_sim_T,n_per=64,task='OBSERVING...'); tot_i_t = 0
                for i_h, (sim_t_, sim_az_, sim_el_, h, p_, o_) in enumerate(zip(self.sim_t_, self.sim_az_, self.sim_el_, 
                                                                                self.heights, self.lay_para_, self.lay_orth_)):
                    for i_t, t in enumerate(sim_t_):
                        prog.update(tot_i_t+1); tot_i_t += 1
                        rel_z_ = h*np.exp(1j*(np.pi/2-sim_az_[:,i_t])) / np.tan(sim_el_[:,i_t])*np.exp(1j*(3*np.pi/2 + self.wind_bearing[i_h]))
                        rel_p_, rel_o_ = np.real(rel_z_), np.imag(rel_z_)
                        ip_min, ip_max = np.where(p_ < rel_p_.min())[0][-1], np.where(p_ > rel_p_.max())[0][0] + 1
                        io_min, io_max = np.where(o_ < rel_o_.min())[0][-1], np.where(o_ > rel_o_.max())[0][0] + 1
                        i_p = (p_ > rel_p_.min()) & (p_ < rel_p_.max())
                        i_o = (o_ > rel_o_.min()) & (o_ < rel_o_.max())
                        atm_interp = sp.interpolate.RegularGridInterpolator((p_[ip_min:ip_max], o_[io_min:io_max]), self.gen_data[i_h][i_t:i_t+self.n_para_[i_h]][ip_min:ip_max,io_min:io_max])
                        h_atm_sim_data[i_h][:,i_t] = atm_interp((rel_p_, rel_o_))

            if interp_method=='tree_gaussian':
                self.generate_atmosphere(blurred=False)
                prog = aram_tools.progress_bar(n_total=self.sim_T,n_per=16,task='OBSERVING...')
                for i_h, (kdt, sim_t_, dx_, dy_) in enumerate(zip(self.static_ckdt, self.sim_t_, self.sim_dx_, self.sim_dy_)): 
                    for i_t, t in enumerate(self.sim_t_):
                        prog.update(i_t+1)
                        self.dist_, self.index_ = kdt.query(np.stack([dx_[:,i_t], dy_[:,i_t]]).T, k=sky_per_det)
                        self.weights  = gaussian(self.dist_,self.ang_sig_[:,i_h][:,None])
                        self.weights /= self.weights.sum(axis=1)[:,None]
                        h_atm_sim_data[i_h,:,i_t] = (self.weights*self.gen_data[i_h][i_t:i_t+self.n_para_[i_h]].ravel()[self.index_]).sum(axis=1)

            if interp_method=='brute_gaussian':
                self.generate_atmosphere(blurred=False)
                prog = aram_tools.progress_bar(n_total=self.sim_T,n_per=16,task='OBSERVING...')
                for i_t, t in enumerate(self.sim_t_):
                    prog.update(i_t+1)
                    #for i_h, (h, a_, e_, dx_, dy_) in enumerate(zip(self.heights,self.lay_a_,self.lay_e_,self.lay_dx_,self.lay_dy_)): 
                    for i_h, z in enumerate(self.lay_dz_): 
                        
                        self.dist_    = np.abs(np.subtract.outer(mod.sim_dx_[:,i_t] + 1j*mod.sim_dy_[:,i_t], z.ravel()))
                        self.weights  = gaussian(self.dist_,self.ang_sig_[:,i_h][:,None])
                        self.weights /= self.weights.sum(axis=1)[:,None]
                        h_atm_sim_data[i_h,:,i_t] = np.matmul(self.weights,self.gen_data[i_h][i_t:i_t+self.n_para_[i_h]].ravel())

                        #self.in_fov  = (a_ > self.sim_min_az_[i_t]) & (a_ < self.sim_max_az_[i_t]) & (e_ > self.sim_min_el_[i_t]) & (e_ < self.sim_max_el_[i_t])
                        #self.ckdt    = sp.spatial.cKDTree(np.vstack([thing.ravel() for thing in aram_tools.ae_to_xy(a_[self.in_fov],e_[self.in_fov],self.sim_c_az_[i_t],self.sim_c_el_[i_t])]).T)
                        #dist_,index_ = self.static_ckdt[i_h].query(np.stack([self.sim_dx_[:,i_t], self.sim_dy_[:,i_t]]).T, k=sky_per_det)
                        #weights  = np.exp(-.5*np.square(dist_ / aram_tools.gaussian_beam(h / np.sin(self.sim_el_[:,i_t]),self.w0,l=self.array.wavelength,n=1.003)[:,None]))
                        #print(index_,weights.shape)
                        #weights /= weights.sum(axis=1)[:,None]
                        #h_atm_sim_data[i_h,:,i_t] = (self.gen_data[i_h][i_t:i_t+self.n_para_[i_h]][self.in_fov][index_]*weights).sum(axis=1)

            h_atm_data = np.concatenate([np.concatenate([sp.interpolate.interp1d(sim_t_,atm_sim_data[i_det],kind='quadratic')(self.obs.t_)[None,:] for i_det in range(self.array.n)])[None,:,:] 
                                         for sim_t_, atm_sim_data in zip(self.sim_t_,h_atm_sim_data)])
            var_prof  = np.exp(-2*self.heights/self.half_height)
            var_prof *= np.square(self.atm_rms) / var_prof.sum() 
            atm_data  = (h_atm_data * np.sqrt(var_prof[:,None,None])).sum(axis=0) / self.sim_el_[0][:,0][:,None]
            
        
        '''
        
        if do_cmb:
            
            print('generating CMB...'); clear_output(wait=True)
            min_ra, max_ra   = np.degrees(self.sp_ra).min(), np.degrees(self.sp_ra).max()
            min_dec, max_dec = np.degrees(self.sp_dec).min(), np.degrees(self.sp_dec).max()

            d_ra  = np.degrees(self.array.fwhm.min())
            d_dec = np.degrees(self.array.fwhm.min())

            self.ra_bins  = np.arange(min_ra, max_ra + d_ra, d_ra)
            self.dec_bins = np.arange(min_dec, max_dec + d_dec, d_dec)
            self.ra_mids  = self.ra_bins[1:]/2 + self.ra_bins[:-1]/2
            self.dec_mids = self.dec_bins[1:]/2 + self.dec_bins[:-1]/2
            self.RA, self.DEC  = np.meshgrid(self.ra_mids, self.dec_mids)
            CMBRA, CMBDEC, CMB = aram_tools.sim_cmb(min_ra, max_ra, min_dec, max_dec, fwhm=np.radians(self.array.fwhm.min()), nside=2048, d_ra=d_ra, d_dec=d_dec, kind='TT')
            
            print('observing CMB...'); clear_output(wait=True)
            cmb_sim_data = sp.interpolate.RegularGridInterpolator((CMBRA[0],CMBDEC[:,0]), 1e-3 * CMB.T)((np.degrees(self.sim_ra_),np.degrees(self.sim_dec_)))
            cmb_data     = np.concatenate([sp.interpolate.interp1d(self.sim_t_,cmb_sim_data[i_det],kind='quadratic')(self.obs.t_)[None,:] for i_det in range(self.array.n)])
            #tot_data    += wnl * np.random.standard_normal(tot_data.shape)
            
        '''
            
        if do_noise:
            
            # simulate white noise
            white_noise = self.array.white[:,None] * np.random.standard_normal((self.array.n,self.obs.T))
            
            # simulate pink noise
            pn_ps       = 1 / (self.obs.f_ + 1e-32); pn_ps[0] = 0 # pink spectrum
            pink_noise  = np.concatenate([np.imag(np.fft.fft(self.array.pink[i_det] * pn_ps * np.fft.ifft(np.random.standard_normal(self.obs.T),norm='ortho'),norm='ortho'))[None,:] 
                                          for i_det in range(self.array.n)])
            noi_data    = pink_noise + white_noise
            #tot_data    +=  
            
        data = {}
        if do_atmosphere:
            data['atmosphere'] = atm_data
        if do_cmb:
            data['cmb'] = cmb_data
        if do_noise:
            data['noise'] = noi_data

        return data
    
    
'''
class tod():
    def __init__(self, data, offset_x, offset_y, t_, az_, el_):
        
        tod.data     = data
        tod.x, tod.y = offset_x, offset_y
        tod.time, tod.freq, tod.az, tod.el = t_, np.fft.fftfreq(len(t_),np.gradient(t_).mean()), az_, el_
        
    def power_spectrum(which,bins=None):
        
        tod.spectrum = np.fft.fft()
        
    def structure_function()
'''
