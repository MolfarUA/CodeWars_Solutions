function ptotal(M₁, M₂, m₁, m₂, V, T)
    (m₁ / M₁ + m₂ / M₂) * (T + 273.15) * 0.082 / V
end

###########
function ptotal(M₁, M₂, m₁, m₂, V, T)
    (m₁/M₁ + m₂/M₂) * 0.082 * (T + 273.15) / V
end

##############
function ptotal(M1, M2, m1, m2, V, T)
    (m1/M1+m2/M2)*0.082*(T+273.15)/V
end

############
function ptotal(M₁, M₂, m₁, m₂, V, T)
    P = (m₁/M₁ + m₂/M₂) * 0.082 * (T + 273.15) / V
  return P
end

###########
ptotal(M₁, M₂, m₁, m₂, V, T) = (m₁ / M₁ + m₂ / M₂) * 0.082 * (T + 273.15) / V

#############
function ptotal(M₁, M₂, m₁, m₂, V, T)
    # your code goes here
  R=0.082
  K=T+273.15
  (m₁/M₁+m₂/M₂)R*K/V
end
