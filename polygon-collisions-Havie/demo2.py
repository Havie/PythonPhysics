#repulsive forces arent good enough for fast collisions 
#need a small enough timestemp to integrate the motion of squeezing 2gether and pushing apart
# or the result will be inaccurate 




#with a collision we only care about final result after 
#make sure momenteum is conserved 
#change in energy is controlled 
    #zero change in KE = elastic collision 
    #decrease in Energy = inelastic collision
    #controlled by coefficient vars 



#step in a collision : 
    #detect overlap 
    #resolve collision
        #resolve overlap
        #resolve velocity 


#collision overlap detection :
    #A-priorty- look ahead and predict when will collide (wont do, more complex/better)
    #n_hat = normalized unit vector orthogonal to floor? idk

    #r= pos_a - pos_b
    #d= Rad_a + Rad_b - mag(r)
    #n_hat = r.normalized()

    #in contact there are normal and friction forces 
    #normal perpendicular to surface
    #friction = parallel to surface


#resolve collision:
    #resolve overlap:
        #shift them so they are just touching
        #shift obj a in -n_hat and object b in +n_hat scaled by d where d is the dis of overlap
        #need to take into account mass/inertia , do so by:
            #keeping the center of the mass unchanged (heavier things move less)
            #amnt of shift proportional to 1/m 
            # change in a.pos = [ 1/mass_a ) / (1/mass_a + 1/mass_b) ] * d(-n_hat)
            # change in b.pos = [ 1/mass_b ) / (1/mass_a + 1/mass_b) ] * d(-n_hat)
            #can replace one part in eqn by letter m, where m = 1/ (1/mass_a + 1/mass_b)   "reduced mass"


    #resolve the velocities: 
        #conserve momenteum 
            #apply same change to each particle "impulse" 
            #equal and opposite impulses
        #correct coefficient of restituiton 
            # e= epsilon 
            # 1D: 
            # e= - velo_final / velo_init in the normal dir 
            # e= - (v_f / v_i )
            # 2D: 
            # v_in = V_i * n_hat 
            # v_fn = V_f * n_hat 
            # e= - (V_fn / V_in)
            # or 
            # v_fn= -e* v_in

        #correct change in direction  
            #"impulse in the normal dir" 


        #what makes the velocity change?:
            #an impulse = J 
            # our J will always be in normal dir
            # J = J_n_hat 
            #change in mommentum = p 
            # p = J
            # pa = J
            # pb = -J
            #change in v_a = J/mass_a
            #change in v_b = -J/mass_b
            #v_af - v_ai = J/mass_a
            #v_bf - v_bi = J/mass_b
            #look at relative velo = : 
            # v= v_a - v_b 
            #v_i = v_ai - v_bi 
            #v_f = v_af - v_bf 
            # so: 
            # v_af - v_bf - ( v_ai - v_bi) = J/mass_a + J/mass_b
            #factor something out: 
            # change in velo = (1/mass_a + 1/mass_b) ( J
            # then multiply by n_hat on both sides and simply to reduced mass: 
            # change in v_n  = J_n / m

            #since   v_fn= -e* v_in from above 
            #set equal 
            #  v_fn= -e* v_in =  J_n / m 
            # J_n = -(1+e) * v_in 
            # J = -(1+e) * v_in * n_hat
            # J = [-(1+e) * (v_ai - v_bi) * n_hat] * n_hat 
            # Apply J to something 




# changes to particle class : 
def impulse(self, impulse):
    self.velo += impulse /self.mass 


















