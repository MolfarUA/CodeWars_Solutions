#![allow(dead_code)]

/// so, when are two type, `a` and `b`, considered equal?
/// a definition might be, it is possible to go from `a` to `b`,
/// and from `b` to `a`.
/// Going a roundway trip should leave you the same value.
/// Unfortunately it is virtually impossible to test this in Haskell,
/// neither in Rust.
/// This is called ISO.
pub enum Void { }

impl PartialEq for Void {
    fn eq(&self, _: &Void) -> bool {
        true
    }
}

pub fn absurd(_: Void) -> ! {
    panic!("You must be kidding! Where did you find that void instance?");
}

pub type Func<A, B> = Box<Fn(A) -> B>;
pub type RetFunc<A, B> = Box<FnOnce(A) -> B>;
pub type ISO<A: 'static, B: 'static> = (Func<A, B>, Func<B, A>);

pub fn iso<A: 'static, B: 'static, F1, F2>(a: F1, b: F2) -> ISO<A, B>
    where F1: 'static + Fn(A) -> B,
          F2: 'static + Fn(B) -> A,
{
    (Box::new(a), Box::new(b))
}

///  *** MENTION ***  ///
///  paste your code  ///
/// from isomorphism  ///
///  *** MENTION ***  ///

/// given ISO a b, we can go from a to b
pub fn sub_st_l<A, B>(iso: ISO<A, B>) -> Box<Fn(A) -> B> { iso.0 }

/// and vice versa
pub fn sub_st_r<A, B>(iso: ISO<A, B>) -> Box<Fn(B) -> A> { iso.1 }

/// There can be more than one ISO a b
pub fn iso_bool() -> ISO<bool, bool> {
    iso::<bool, bool, Box<_>, Box<_>>(Box::new(|a| a), Box::new(|a| a))
}

pub fn iso_bool_not() -> ISO<bool, bool> {
    iso::<bool, bool, Box<_>, Box<_>>(Box::new(|a: bool| !a), Box::new(|a: bool| !a))
}

/// isomorphism is reflexive
pub fn refl<A: 'static>() -> ISO<A, A> {
    iso::<A, A, Box<_>, Box<_>>(Box::new(|a| a), Box::new(|a| a))
}

/// isomorphism is symmetric
pub fn symm<A: 'static, B: 'static>(i: ISO<A, B>) -> ISO<B, A> {
    iso::<B, A, Box<_>, Box<_>>(i.1, i.0)
}

/// isomorphism is transitive
pub fn trans<A: 'static, B: 'static, C: 'static>
    (ab: ISO<A, B>, bc: ISO<B, C>) -> ISO<A, C> {
        let a_to_b = ab.0;
        let b_to_a = ab.1;
        let b_to_c = bc.0;
        let c_to_b = bc.1;
        let a_to_c = move |a: A|{
             b_to_c(a_to_b(a))  
        };
        let c_to_a = move |c: C|{
            b_to_a(c_to_b(c))
        };
        iso::<A, C, Box<_>, Box<_>>(Box::new(a_to_c), Box::new(c_to_a))
    }

/// we can combine isomorphism
pub fn iso_tuple<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<(A, C), (B, D)> {
        let a_to_b = ab.0;
        let b_to_a = ab.1;
        let c_to_d = cd.0;
        let d_to_c = cd.1;
        let ac_to_bd = move |ac:(A, C)|{
            (a_to_b(ac.0), c_to_d(ac.1))
        };
        let bd_to_ac = move |bd:(B, D)|{
            (b_to_a(bd.0), d_to_c(bd.1))  
        };
        iso::<(A, C), (B, D), Box<_>, Box<_>>(Box::new(ac_to_bd), Box::new(bd_to_ac))
    }

pub fn iso_vec<A: 'static, B: 'static>(i: ISO<A, B>) -> ISO<Vec<A>, Vec<B>> {
    let a_to_b = i.0;
    let b_to_a = i.1;
    let va_to_vb = move |va: Vec<A>|{
        let mut vb = Vec::new();
        for i in va{
            vb.push(a_to_b(i));
        }
        vb
    };
    let vb_to_va = move |vb: Vec<B>|{
        let mut va = Vec::new();
        for i in vb{
            va.push(b_to_a(i));
        }
        va
    };
    iso::<Vec<A>, Vec<B>, Box<_>, Box<_>>(Box::new(va_to_vb), Box::new(vb_to_va))
}

pub fn iso_option<A: 'static, B: 'static>
    (i: ISO<A, B>) -> ISO<Option<A>, Option<B>> {
        let a_to_b = i.0;
        let b_to_a = i.1;
        let oa_to_ob = move |oa: Option<A>|{
            match oa{
                Some(a) => Some(a_to_b(a)),
                None => None
            }
        };
        let ob_to_oa = move |ob: Option<B>|{
            match ob{
                Some(b) => Some(b_to_a(b)),
                None => None
            }
        };
        iso::<Option<A>, Option<B>, Box<_>, Box<_>>(Box::new(oa_to_ob), Box::new(ob_to_oa))
    }

pub fn iso_result<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>> {
        let a_to_b = ab.0;
        let b_to_a = ab.1;
        let c_to_d = cd.0;
        let d_to_c = cd.1;
        let rac_to_rbd = move |rac: Result<A, C>|{
            match rac{
                Ok(a) => Ok(a_to_b(a)),
                Err(c) => Err(c_to_d(c)),
            }  
        };
        let rbd_to_rac = move |rbd: Result<B, D>|{
            match rbd{
                Ok(b) => Ok(b_to_a(b)),
                Err(d) => Err(d_to_c(d)),
            }
        };
        iso::<Result<A, C>, Result<B, D>, Box<_>, Box<_>>(Box::new(rac_to_rbd), Box::new(rbd_to_rac))
    }

/// Going another way is hard (and is generally impossible)
/// Remember, for all valid ISO, converting and converting back
/// is the same as the original value.
/// You need this to prove some case are impossible.
pub fn iso_un_option<A: 'static, B: 'static>
    (i: ISO<Option<A>, Option<B>>) -> ISO<A, B> {
        let oa_to_ob = i.0;
        let ob_to_oa = i.1;
        let a_to_b = move |a: A|{
            let ob = oa_to_ob(Some(a));
            if let Some(b) = ob{
                b
            }else {
                oa_to_ob(None).unwrap()
            }
        };
        let b_to_a = move |b: B|{
            let oa = ob_to_oa(Some(b));
            if let Some(a) = oa{
                a
            }else {
                ob_to_oa(None).unwrap()
            }
        };
        iso::<A, B, Box<_>, Box<_>>(Box::new(a_to_b), Box::new(b_to_a))
    }

/// inf + 0 = inf + 1
pub fn iso_eu() -> ISO<Result<Vec<()>, ()>, Result<Vec<()>, Void>> {
    let a_to_b = move |a: Result<Vec<()>, ()>|{
        let length = match a {
            Ok(vec) => vec.len()+1,
            Err(_) => 0
        };
        let mut b = Vec::new();
        for i in 0..length{
            b.push(());
        }
        Ok(b)
    };
    let b_to_a = move |b: Result<Vec<()>, Void>|{
        match b{
            Ok(vec) => {
                let length = vec.len();
                if length == 0{
                    Err(())
                }else{
                    let mut a = Vec::new();
                    for i in 0..length-1{
                        a.push(());
                    }
                    Ok(a)    
                }
            },
            Err(_) => Err(())  
        }
    };
    iso::<Result<Vec<()>, ()>, Result<Vec<()>, Void>, Box<_>, Box<_>>(Box::new(a_to_b), Box::new(b_to_a))
}

pub type IsoFL<A, B, C, D> = Box<FnOnce(Box<Fn(A) -> C>) -> Box<FnOnce(B) -> D>>;
pub type IsoFR<A, B, C, D> = Box<FnOnce(Box<Fn(B) -> D>) -> Box<FnOnce(A) -> C>>;
pub type IsoF<A, B, C, D> = (IsoFL<A, B, C, D>, IsoFR<A, B, C, D>);

/// translator note:
/// FnBox is not yet supported, we can only return an uncallable
/// Box<FnOnce> (RetFunc). You should return the function with
/// correct type, which will be checked by the tests.
/// The type annotation is shown above. You need you return something like
/// (Box::new(...), Box::new(...))
pub fn iso_func<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> IsoF<A, B, C, D> {
        let a_to_b = ab.0;
        let b_to_a = ab.1;
        let c_to_d = cd.0;
        let d_to_c = cd.1;
        let fl: IsoFL<A, B, C, D> = Box::new(move |a_to_c: Box<Fn(A) -> C>|{
            Box::new(move |b: B|{
                c_to_d(a_to_c(b_to_a(b)))
            })
        });
        let fr: IsoFR<A, B, C, D> = Box::new(move |b_to_d: Box<Fn(B) -> D>|{
            Box::new(move |a: A|{
                d_to_c(b_to_d(a_to_b(a)))
            })
        });
        (fl, fr)
    }

/// And we have isomorphism on isomorphism!
pub fn iso_symm<A: 'static, B: 'static>() -> ISO<ISO<A, B>, ISO<B, A>> {
    let iab_to_iba = move |iab: ISO<A, B>|{
        iso::<B, A, Box<_>, Box<_>>(iab.1, iab.0)
    };
    let iba_to_iab = move |iba: ISO<B, A>|{
        iso::<A, B, Box<_>, Box<_>>(iba.1, iba.0)  
    };
    iso::<ISO<A, B>, ISO<B, A>, Box<_>, Box<_>>(Box::new(iab_to_iba), Box::new(iba_to_iab))
}

/// Sometimes, we can treat a Type as a Number:
/// if a Type t has n distinct value, it's Number is n.
/// This is formally called cardinality.
/// See https://en.wikipedia.org/wiki/Cardinality
///
/// Void has cardinality of 0 (we will abbreviate it Void is 0).
/// () is 1.
/// Bool is 2.
/// Maybe a is 1 + a.
/// We will be using peano arithmetic so we will write it as S a.
/// https://en.wikipedia.org/wiki/Peano_axioms
/// Either a b is a + b.
/// (a, b) is a * b.
/// a => b is b ^ a. Try counting (() => Bool) and (Bool => ())
///
/// Algebraic data type got the name because
/// it satisfies a lot of algebraic rules under isomorphism    

/// a = b => c = d => a * c = b * d
pub fn iso_prod<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<(A, C), (B, D)> {
        iso_tuple(ab, cd)
    }

/// a = b => c = d => a + c = b + d
pub fn iso_plus<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>> {
        iso_result(ab, cd)
    }

/// a = b => S a = S b
pub fn iso_s<A: 'static, B: 'static>
    (i: ISO<A, B>) -> ISO<Option<A>, Option<B>> {
        iso_option(i)
    }

/// a = b => c = d => c ^ a = d ^ b
pub fn iso_pow<A: 'static, B: 'static, C: 'static, D: 'static>
    (ab: ISO<A, B>, cd: ISO<C, D>) -> IsoF<A, B, C, D> {
        iso_func(ab, cd)
    }

/// a + b = b + a
pub fn plus_comm<A: 'static, B: 'static>() -> ISO<Result<A, B>, Result<B, A>> {
    let first = |input: Result<A, B>|{
        match input{
            Ok(a) => Err(a),
            Err(b) => Ok(b)
        }
    };
    let second = |input: Result<B, A>|{
        match input{
            Ok(b) => Err(b),
            Err(a) => Ok(a)
        }  
    };
    iso::<Result<A, B>, Result<B, A>, Box<_>, Box<_>>(Box::new(first), Box::new(second))
}

/// a + b + c = a + (b + c)
pub fn plus_assoc<A: 'static, B: 'static, C: 'static>
    () -> ISO<Result<Result<A, B>, C>, Result<A, Result<B, C>>> {
        let first = |input: Result<Result<A, B>, C>|{
            match input{
                Ok(ab) => match ab{
                    Ok(a) => Ok(a),
                    Err(b) => Err(Ok(b))
                },
                Err(c) => Err(Err(c))
            }
        };
        let second = |input: Result<A, Result<B, C>>|{
            match input{
                Ok(a) => Ok(Ok(a)),
                Err(bc) => match bc{
                    Ok(b) => Ok(Err(b)),
                    Err(c) => Err(c)
                }
            }
        };
        iso::<Result<Result<A, B>, C>, Result<A, Result<B, C>>, Box<_>, Box<_>>(Box::new(first), Box::new(second))
    }

/// a * b = b * a
pub fn mult_comm<A: 'static, B: 'static>() -> ISO<(A, B), (B, A)> {
    let first = |input: (A, B)|{
        (input.1, input.0)  
    };
    let second = |input: (B, A)|{
        (input.1, input.0)
    };
    iso::<(A, B), (B, A), Box<_>, Box<_>>(Box::new(first), Box::new(second))
}

/// a * b * c = a * (b * c)
pub fn mult_assoc<A: 'static, B: 'static, C: 'static>
    () -> ISO<((A, B), C), (A, (B, C))> {
        let first = |input: ((A, B), C)|{
            ((input.0).0, ((input.0).1, input.1))  
        };
        let second = |input: (A, (B, C))|{
            ((input.0, (input.1).0), (input.1).1)   
        };
        iso::<((A, B), C), (A, (B, C)), Box<_>, Box<_>>(Box::new(first), Box::new(second))
    }

/// a * (b + c) = a * b + a * c
pub fn dist<A: 'static, B: 'static, C: 'static>
    () -> ISO<(A, Result<B, C>), Result<(A, B), (A, C)>> {
        let first = |input: (A, Result<B, C>)|{
            match input.1{
                Ok(b) => Ok((input.0, b)),
                Err(c) => Err((input.0, c))
            }  
        };
        let second = |input: Result<(A, B), (A, C)>|{
            match input{
                Ok(ab) => (ab.0, Ok(ab.1)),
                Err(ac) => (ac.0, Err(ac.1)), 
            }
        };
        iso::<(A, Result<B, C>), Result<(A, B), (A, C)>, Box<_>, Box<_>>(Box::new(first), Box::new(second))
}

pub type IsoCL<A, B, C> = RetFunc<Func<A, Func<B, C>>, RetFunc<(A, B), C>>;
pub type IsoCR<A, B, C> = RetFunc<Func<(A, B), C>, RetFunc<A, RetFunc<B, C>>>;
pub type IsoC<A, B, C> = (IsoCL<A, B, C>, IsoCR<A, B, C>);

/// translator note:
/// FnBox is not yet supported, we can only return an uncallable
/// Box<FnOnce> (RetFunc). You should return the function with
/// correct type, which will be checked by the tests.
/// later you'll have to implement three more functions that related
/// to `RetFunc`. enjoy!

/// (c ^ b) ^ a = c ^ (a * b)
pub fn curry_iso<A: 'static, B: 'static, C: 'static>() -> IsoC<A, B, C> {
    let iso_cl: IsoCL<A, B, C> = Box::new(|input: Func<A, Func<B, C>>|{
        Box::new(move |ab: (A, B)|{
            (input(ab.0))(ab.1)
        })
    });
    let iso_cr: IsoCR<A, B, C> = Box::new(|input: Func<(A, B), C>|{
        Box::new(move |a: A|{
            Box::new(move |b: B|{
                input((a, b))
            })
        })  
    });
    (iso_cl, iso_cr)
}

/// 1 = S O (we are using peano arithmetic)
/// https://en.wikipedia.org/wiki/Peano_axioms  
pub fn one() -> ISO<(), Option<Void>> {
    let a_to_b = |a : ()|{
        None
    };
    let b_to_a = |b : Option<Void>|{
        match b{
            Some(v) => absurd(v),
            None => ()
        }
    };
    iso::<(), Option<Void>, Box<_>, Box<_>>(Box::new(a_to_b), Box::new(b_to_a))
}

/// 2 = S (S O)
pub fn two() -> ISO<bool, Option<Option<Void>>> {
    let bool_to_option = |a: bool|{
        if a{
            None
        }else{
            Some(None)
        }
    };
    let option_to_bool = |a: Option<Option<Void>>| {
        match a{
            None => true,
            Some(b) => match b{
                None => false,
                Some(void) => absurd(void)
            }
        }    
    };
    iso::<bool, Option<Option<Void>>, Box<_>, Box<_>>(Box::new(bool_to_option), Box::new(option_to_bool))
}

/// 0 + b = b
pub fn plus_o<B: 'static>() -> ISO<Result<Void, B>, B> {
    let a_to_b = |a: Result<Void, B>|{
        match a{
            Ok(void) => absurd(void),
            Err(b) => b 
        }
    };
    let b_to_a = |b: B|{
        Err(b)
    };
    iso::<Result<Void, B>, B, Box<_>, Box<_>>(Box::new(a_to_b), Box::new(b_to_a))
}

/// S a + b = S (a + b)
pub fn plus_s<A: 'static, B: 'static>
    () -> ISO<Result<Option<A>, B>, Option<Result<A, B>>> {
        let first = |input: Result<Option<A>, B>|{
            match input{
                Ok(oa) => match oa{
                    Some(a) => Some(Ok(a)),
                    None => None
                },
                Err(b) => Some(Err(b)),
            }
        };
        let second = |input: Option<Result<A, B>>|{
            match input {
                Some(rab) => match rab{
                    Ok(a) => Ok(Some(a)),
                    Err(b) => Err(b),
                },
                None => Ok(None),
            }
        };
        iso::<Result<Option<A>, B>, Option<Result<A, B>>, Box<_>, Box<_>>(Box::new(first), Box::new(second))
    }

/// 1 + b = S b
pub fn plus_so<B: 'static>() -> ISO<Result<(), B>, Option<B>> {
    trans(iso_plus(one(), refl()),
          trans(plus_s(), iso_s(plus_o())))
}

/// 0 * a = 0
pub fn mult_o<A: 'static>() -> ISO<(Void, A), Void> {
    let first = |input: (Void, A)|{
        absurd(input.0)  
    };
    let second = |input: Void|{
        absurd(input)
    };
    iso::<(Void, A), Void, Box<_>, Box<_>>(Box::new(first), Box::new(second))
}

/// S a * b = b + a * b
pub fn mult_s<A: 'static, B: 'static>
    () -> ISO<(Option<A>, B), Result<B, (A, B)>> {
        let first = |input: (Option<A>, B)|{
            match input.0{
                Some(a) => Err((a, input.1)),
                None => Ok(input.1)
            }
        };
        let second = |input: Result<B, (A, B)>|{
            match input{
                Ok(b) => (None, b),
                Err(ab) => (Some(ab.0), ab.1)
            }  
        };
        iso::<(Option<A>, B), Result<B, (A, B)>, Box<_>, Box<_>>(Box::new(first), Box::new(second))
    }

/// S a * b = b + a * b
pub fn mult_so<B: 'static>() -> ISO<((), B), B> {
    trans(iso_prod(one(), refl()),
          trans(mult_s(),
                trans(iso_plus(refl(), mult_o()),
                      trans(plus_comm(), plus_o()))))
}

/// Here we go, the last three functions related to
/// RetFunc. They're easy!

pub type IsoPL<A> = RetFunc<Func<Void, A>, ()>;
pub type IsoPR<A> = RetFunc<(), RetFunc<Void, A>>;
pub type IsoP<A> = (IsoPL<A>, IsoPR<A>);

/// a ^ 0 = 1
pub fn pow_o<A: 'static>() -> IsoP<A> {
    let iso_pl: IsoPL<A> = Box::new(|_: Func<Void, A>|{
        ()
    });
    let iso_pr: IsoPR<A> = Box::new(|_: ()|{
       Box::new(|input: Void|{
           absurd(input)
        }) 
    });
    (iso_pl, iso_pr)
}

pub type IsoPsL<A, B> = RetFunc<Func<Option<B>, A>, (A, RetFunc<B, A>)>;
pub type IsoPsR<A, B> = RetFunc<(A, Func<B, A>), RetFunc<Option<B>, A>>;
pub type IsoPs<A, B> = (IsoPsL<A, B>, IsoPsR<A, B>);

/// a ^ (S b) = a * (a ^ b)
pub fn pow_s<A: 'static, B: 'static>() -> IsoPs<A, B> {
    let iso_psl: IsoPsL<A, B> = Box::new(|input: Func<Option<B>, A>|{
        let a = input(None);
        let func = Box::new(move |b: B|{
            input(Some(b))
        });
        (a, func)
    });
    let iso_psr: IsoPsR<A, B> = Box::new(|input: (A, Func<B, A>)|{
        Box::new(|ob: Option<B>|{
            match ob{
                Some(b) => (input.1)(b),
                None => input.0
            }
        })
    });
    (iso_psl, iso_psr)
}

pub type IsoPsoL<A> = RetFunc<Func<(), A>, A>;
pub type IsoPsoR<A> = RetFunc<A, RetFunc<(), A>>;
pub type IsoPso<A> = (IsoPsoL<A>, IsoPsoR<A>);

/// a ^ 1 = a
/// In Haskell/Java/Dart, you can go the hard way
/// (like mult_so, plus_so) to prove that you really get what is
/// going on.
/// Unfortunately, in Rust, you can only go the trivial way.
/// Because Rust doesn't support FnBox ATM.
pub fn pow_so<A: 'static>() -> IsoPso<A> {
    let iso_psol: IsoPsoL<A> = Box::new(|input: Func<(), A>|{
        input(())
    });
    let iso_psor: IsoPsoR<A> = Box::new(|input: A|{
        Box::new(|_: ()|{
            input
        })
    });
    (iso_psol, iso_psor)
}

_________________________________________________________________
#![allow(dead_code)]

/// so, when are two type, `a` and `b`, considered equal?
/// a definition might be, it is possible to go from `a` to `b`,
/// and from `b` to `a`.
/// Going a roundway trip should leave you the same value.
/// Unfortunately it is virtually impossible to test this in Haskell,
/// neither in Rust.
/// This is called ISO.
pub enum Void {}

impl PartialEq for Void {
    fn eq(&self, _: &Void) -> bool {
        true
    }
}

pub fn absurd(_: Void) -> ! {
    panic!("You must be kidding! Where did you find that void instance?");
}

pub type Func<A, B> = Box<Fn(A) -> B>;
pub type RetFunc<A, B> = Box<FnOnce(A) -> B>;
pub type ISO<A: 'static, B: 'static> = (Func<A, B>, Func<B, A>);

pub fn iso<A: 'static, B: 'static, F1, F2>(a: F1, b: F2) -> ISO<A, B>
    where F1: 'static + Fn(A) -> B,
          F2: 'static + Fn(B) -> A, {
    (Box::new(a), Box::new(b))
}

///  *** MENTION ***  ///
///  paste your code  ///
/// from isomorphism  ///
///  *** MENTION ***  ///

pub fn sub_st_l<A: 'static, B: 'static>
((ab, _): ISO<A, B>) -> Func<A, B> {
    ab
}

pub fn sub_st_r<A: 'static, B: 'static>
((_, ba): ISO<A, B>) -> Func<B, A> {
    ba
}

pub fn refl<A: 'static>
() -> ISO<A, A> {
    iso(
        |a| a,
        |a| a,
    )
}

pub fn symm<A: 'static, B: 'static>
((ab, ba): ISO<A, B>) -> ISO<B, A> {
    iso(ba, ab)
}

pub fn trans<A: 'static, B: 'static, C: 'static>
((ab, ba): ISO<A, B>, (bc, cb): ISO<B, C>) -> ISO<A, C> {
    iso(
        move |a| bc(ab(a)),
        move |c| ba(cb(c)),
    )
}

pub fn iso_bool() -> ISO<bool, bool> {
    iso(
        |x| x,
        |x| x,
    )
}

pub fn iso_bool_not() -> ISO<bool, bool> {
    iso(
        |x: bool| !x,
        |x: bool| !x,
    )
}

pub fn iso_tuple<A: 'static, B: 'static, C: 'static, D: 'static>
((ab, ba): ISO<A, B>, (cd, dc): ISO<C, D>) -> ISO<(A, C), (B, D)> {
    iso(
        move |(a, c)| (ab(a), cd(c)),
        move |(b, d)| (ba(b), dc(d)),
    )
}

pub fn iso_vec<A: 'static, B: 'static>((ab, ba): ISO<A, B>) -> ISO<Vec<A>, Vec<B>> {
    iso(
        move |mut va: Vec<A>| va.drain(..).map(|a| ab(a)).collect(),
        move |mut vb: Vec<B>| vb.drain(..).map(|b| ba(b)).collect(),
    )
}

pub fn iso_option<A: 'static, B: 'static>
((ab, ba): ISO<A, B>) -> ISO<Option<A>, Option<B>> {
    iso(
        move |oa| match oa {
            Some(a) => Some(ab(a)),
            None => None,
        },
        move |ob| match ob {
            Some(b) => Some(ba(b)),
            None => None,
        },
    )
}

pub fn iso_result<A: 'static, B: 'static, C: 'static, D: 'static>
((ab, ba): ISO<A, B>, (cd, dc): ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>> {
    iso(
        move |r| match r {
            Ok(a) => Ok(ab(a)),
            Err(c) => Err(cd(c)),
        },
        move |r| match r {
            Ok(b) => Ok(ba(b)),
            Err(d) => Err(dc(d)),
        },
    )
}

pub fn iso_un_option<A: 'static, B: 'static>
((oaob, oboa): ISO<Option<A>, Option<B>>) -> ISO<A, B> {
    iso(
        move |a| match oaob(Some(a)) {
            Some(b) => b,
            None => match oaob(None) {
                Some(b) => b,
                None => panic!("impossible"),
            }
        },
        move |b| match oboa(Some(b)) {
            Some(a) => a,
            None => match oboa(None) {
                Some(a) => a,
                None => panic!("impossible"),
            }
        },
    )
}

pub fn iso_eu() -> ISO<Result<Vec<()>, ()>, Result<Vec<()>, Void>> {
    iso(
        |r: Result<Vec<()>, ()>| match r {
            Ok(mut v) => {
                v.push(());
                Ok(v)
            }
            Err(_) => Ok(vec![]),
        },
        |r: Result<Vec<()>, Void>| match r {
            Ok(mut v) => if v.is_empty() {
                Err(())
            } else {
                v.pop();
                Ok(v)
            }
            Err(v) => absurd(v),
        },
    )
}

pub type IsoFL<A, B, C, D> = Box<FnOnce(Box<Fn(A) -> C>) -> Box<FnOnce(B) -> D>>;
pub type IsoFR<A, B, C, D> = Box<FnOnce(Box<Fn(B) -> D>) -> Box<FnOnce(A) -> C>>;
pub type IsoF<A, B, C, D> = (IsoFL<A, B, C, D>, IsoFR<A, B, C, D>);

pub fn iso_func<A: 'static, B: 'static, C: 'static, D: 'static>
((ab, ba): ISO<A, B>, (cd, dc): ISO<C, D>) -> IsoF<A, B, C, D> {
    (
        Box::new(move |ac: Func<A, C>| Box::new(move |b| cd(ac(ba(b))))),
        Box::new(move |bd: Func<B, D>| Box::new(move |a| dc(bd(ab(a))))),
    )
}

pub fn iso_symm<A: 'static, B: 'static>() -> ISO<ISO<A, B>, ISO<B, A>> {
    iso(
        |(ab, ba)| (ba, ab),
        |(ba, ab)| (ab, ba),
    )
}

/// Sometimes, we can treat a Type as a Number:
/// if a Type t has n distinct value, it's Number is n.
/// This is formally called cardinality.
/// See https://en.wikipedia.org/wiki/Cardinality
///
/// Void has cardinality of 0 (we will abbreviate it Void is 0).
/// () is 1.
/// Bool is 2.
/// Maybe a is 1 + a.
/// We will be using peano arithmetic so we will write it as S a.
/// https://en.wikipedia.org/wiki/Peano_axioms
/// Either a b is a + b.
/// (a, b) is a * b.
/// a => b is b ^ a. Try counting (() => Bool) and (Bool => ())
///
/// Algebraic data type got the name because
/// it satisfies a lot of algebraic rules under isomorphism

/// a = b => c = d => a * c = b * d
pub fn iso_prod<A: 'static, B: 'static, C: 'static, D: 'static>
(ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<(A, C), (B, D)> {
    iso_tuple(ab, cd)
}

/// a = b => c = d => a + c = b + d
pub fn iso_plus<A: 'static, B: 'static, C: 'static, D: 'static>
(ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>> {
    iso_result(ab, cd)
}

/// a = b => S a = S b
pub fn iso_s<A: 'static, B: 'static>
(i: ISO<A, B>) -> ISO<Option<A>, Option<B>> {
    iso_option(i)
}

/// a = b => c = d => c ^ a = d ^ b
pub fn iso_pow<A: 'static, B: 'static, C: 'static, D: 'static>
(ab: ISO<A, B>, cd: ISO<C, D>) -> IsoF<A, B, C, D> {
    iso_func(ab, cd)
}

/// a + b = b + a
pub fn plus_comm<A: 'static, B: 'static>() -> ISO<Result<A, B>, Result<B, A>> {
    iso(
        |r| match r {
            Ok(a) => Err(a),
            Err(b) => Ok(b),
        },
        |r| match r {
            Ok(b) => Err(b),
            Err(a) => Ok(a),
        },
    )
}

/// a + b + c = a + (b + c)
pub fn plus_assoc<A: 'static, B: 'static, C: 'static>
() -> ISO<Result<Result<A, B>, C>, Result<A, Result<B, C>>> {
    iso(
        |r| match r {
            Ok(ab) => match ab {
                Ok(a) => Ok(a),
                Err(b) => Err(Ok(b)),
            },
            Err(c) => Err(Err(c)),
        },
        |r| match r {
            Ok(a) => Ok(Ok(a)),
            Err(bc) => match bc {
                Ok(b) => Ok(Err(b)),
                Err(c) => Err(c),
            },
        },
    )
}

/// a * b = b * a
pub fn mult_comm<A: 'static, B: 'static>() -> ISO<(A, B), (B, A)> {
    iso(
        |(a, b)| (b, a),
        |(b, a)| (a, b),
    )
}

/// a * b * c = a * (b * c)
pub fn mult_assoc<A: 'static, B: 'static, C: 'static>
() -> ISO<((A, B), C), (A, (B, C))> {
    iso(
        |((a, b), c)| (a, (b, c)),
        |(a, (b, c))| ((a, b), c),
    )
}

/// a * (b + c) = a * b + a * c
pub fn dist<A: 'static, B: 'static, C: 'static>
() -> ISO<(A, Result<B, C>), Result<(A, B), (A, C)>> {
    iso(
        |(a, bc)| match bc {
            Ok(b) => Ok((a, b)),
            Err(c) => Err((a, c)),
        },
        |r| match r {
            Ok((a, b)) => (a, Ok(b)),
            Err((a, c)) => (a, Err(c)),
        },
    )
}

pub type IsoCL<A, B, C> = RetFunc<Func<A, Func<B, C>>, RetFunc<(A, B), C>>;
pub type IsoCR<A, B, C> = RetFunc<Func<(A, B), C>, RetFunc<A, RetFunc<B, C>>>;
pub type IsoC<A, B, C> = (IsoCL<A, B, C>, IsoCR<A, B, C>);

/// translator note:
/// FnBox is not yet supported, we can only return an uncallable
/// Box<FnOnce> (RetFunc). You should return the function with
/// correct type, which will be checked by the tests.
/// later you'll have to implement three more functions that related
/// to `RetFunc`. enjoy!

/// (c ^ b) ^ a = c ^ (a * b)
pub fn curry_iso<A: 'static, B: 'static, C: 'static>() -> IsoC<A, B, C> {
    (
        Box::new(|a_bc| Box::new(move |(a, b)| a_bc(a)(b))),
        Box::new(|ab_c| Box::new(|a| Box::new(move |b| ab_c((a, b))))),
    )
}

/// 1 = S O (we are using peano arithmetic)
/// https://en.wikipedia.org/wiki/Peano_axioms
pub fn one() -> ISO<(), Option<Void>> {
    iso(
        |_| None,
        |_| (),
    )
}

/// 2 = S (S O)
pub fn two() -> ISO<bool, Option<Option<Void>>> {
    iso(
        |x| match x {
            true => Some(None),
            false => None,
        },
        |x| match x {
            Some(_) => true,
            None => false,
        },
    )
}

/// 0 + b = b
pub fn plus_o<B: 'static>() -> ISO<Result<Void, B>, B> {
    iso(
        |r| match r {
            Ok(v) => absurd(v),
            Err(b) => b,
        },
        |b| Err(b),
    )
}

/// S a + b = S (a + b)
pub fn plus_s<A: 'static, B: 'static>
() -> ISO<Result<Option<A>, B>, Option<Result<A, B>>> {
    iso(
        |r| match r {
            Ok(oa) => match oa {
                Some(a) => Some(Ok(a)),
                None => None,
            },
            Err(b) => Some(Err(b)),
        },
        |o| match o {
            Some(r) => match r {
                Ok(a) => Ok(Some(a)),
                Err(b) => Err(b),
            },
            None => Ok(None),
        },
    )
}

/// 1 + b = S b
pub fn plus_so<B: 'static>() -> ISO<Result<(), B>, Option<B>> {
    trans(iso_plus(one(), refl()),
          trans(plus_s(), iso_s(plus_o())))
}

/// 0 * a = 0
pub fn mult_o<A: 'static>() -> ISO<(Void, A), Void> {
    iso(
        |(v, _)| v,
        |v| absurd(v),
    )
}

/// S a * b = b + a * b
pub fn mult_s<A: 'static, B: 'static>
() -> ISO<(Option<A>, B), Result<B, (A, B)>> {
    iso(
        |(oa, b)| match oa {
            Some(a) => Err((a, b)),
            None => Ok(b),
        },
        |r| match r {
            Ok(b) => (None, b),
            Err((a, b)) => (Some(a), b),
        },
    )
}

/// S a * b = b + a * b
pub fn mult_so<B: 'static>() -> ISO<((), B), B> {
    trans(iso_prod(one(), refl()),
          trans(mult_s(),
                trans(iso_plus(refl(), mult_o()),
                      trans(plus_comm(), plus_o()))))
}

/// Here we go, the last three functions related to
/// RetFunc. They're easy!

pub type IsoPL<A> = RetFunc<Func<Void, A>, ()>;
pub type IsoPR<A> = RetFunc<(), RetFunc<Void, A>>;
pub type IsoP<A> = (IsoPL<A>, IsoPR<A>);

/// a ^ 0 = 1
pub fn pow_o<A: 'static>() -> IsoP<A> {
    (
        Box::new(|_| ()),
        Box::new(|_| Box::new(|v| absurd(v))),
    )
}

pub type IsoPsL<A, B> = RetFunc<Func<Option<B>, A>, (A, RetFunc<B, A>)>;
pub type IsoPsR<A, B> = RetFunc<(A, Func<B, A>), RetFunc<Option<B>, A>>;
pub type IsoPs<A, B> = (IsoPsL<A, B>, IsoPsR<A, B>);

/// a ^ (S b) = a * (a ^ b)
pub fn pow_s<A: 'static, B: 'static>() -> IsoPs<A, B> {
    (
        Box::new(|oba|
            (
                oba(None),
                Box::new(move |b| oba(Some(b))),
            )
        ),
        Box::new(|(a, ba)|
            Box::new(move |ob| match ob {
                Some(b) => ba(b),
                None => a,
            })
        ),
    )
}

pub type IsoPsoL<A> = RetFunc<Func<(), A>, A>;
pub type IsoPsoR<A> = RetFunc<A, RetFunc<(), A>>;
pub type IsoPso<A> = (IsoPsoL<A>, IsoPsoR<A>);

/// a ^ 1 = a
/// In Haskell/Java/Dart, you can go the hard way
/// (like mult_so, plus_so) to prove that you really get what is
/// going on.
/// Unfortunately, in Rust, you can only go the trivial way.
/// Because Rust doesn't support FnBox ATM.
pub fn pow_so<A: 'static>() -> IsoPso<A> {
    (
        Box::new(|f| f(())),
        Box::new(|a| Box::new(|_| a)),
    )
}
_________________________________________________________________________________________________
#![allow(dead_code)]

/// so, when are two type, `a` and `b`, considered equal?
/// a definition might be, it is possible to go from `a` to `b`,
/// and from `b` to `a`.
/// Going a roundway trip should leave you the same value.
/// Unfortunately it is virtually impossible to test this in Haskell,
/// neither in Rust.
/// This is called ISO.
pub enum Void { }

impl PartialEq for Void {
    fn eq(&self, _: &Void) -> bool {
        true
    }
}

pub fn absurd(_: Void) -> ! {
    panic!("You must be kidding! Where did you find that void instance?");
}

pub type Func<A, B> = Box<dyn Fn(A) -> B>;
pub type RetFunc<A, B> = Box<dyn FnOnce(A) -> B>;
pub type ISO<A: 'static, B: 'static> = (Func<A, B>, Func<B, A>);

pub fn iso<A: 'static, B: 'static, F1, F2>(a: F1, b: F2) -> ISO<A, B>
    where F1: 'static + Fn(A) -> B,
          F2: 'static + Fn(B) -> A,
{
    (Box::new(a), Box::new(b))
}

/// given ISO a b, we can go from a to b
pub fn sub_st_l<A, B>(iso: ISO<A, B>) -> Box<dyn Fn(A) -> B> { iso.0 }

/// and vice versa
pub fn sub_st_r<A, B>(iso: ISO<A, B>) -> Box<dyn Fn(B) -> A> { iso.1 }

/// There can be more than one ISO a b
pub fn iso_bool() -> ISO<bool, bool> {
    fn f(v: bool) -> bool { v }

    iso(f, f)
}

pub fn iso_bool_not() -> ISO<bool, bool> {
    fn f(v: bool) -> bool { !v }

    iso(f, f)
}

/// isomorphism is reflexive
pub fn refl<A: 'static>() -> ISO<A, A> {
    iso(|a| a, |a| a)
}

/// isomorphism is symmetric
pub fn symm<A: 'static, B: 'static>(i: ISO<A, B>) -> ISO<B, A> {
    iso(i.1, i.0)
}

/// isomorphism is transitive
pub fn trans<A, B, C>((f_ab, g_ab): ISO<A, B>, (f_bc, g_bc): ISO<B, C>) -> ISO<A, C>
    where A: 'static, B: 'static, C: 'static {
    iso(move |x| f_bc(f_ab(x)), move |x| g_ab(g_bc(x)))
}

/// we can combine isomorphism
pub fn iso_tuple<A, B, C, D>((f_ab, g_ab): ISO<A, B>, (f_cd, g_cd): ISO<C, D>) -> ISO<(A, C), (B, D)>
    where A: 'static, B: 'static, C: 'static, D: 'static {
    iso(move |(a, c)| (f_ab(a), f_cd(c)), move |(b, d)| (g_ab(b), g_cd(d)))
}

pub fn iso_vec<A: 'static, B: 'static>((g, h): ISO<A, B>) -> ISO<Vec<A>, Vec<B>> {
    iso(
        move |v: Vec<A>| {let ref f = g; v.into_iter().map(f).collect()},
        move |v: Vec<B>| {let ref f = h; v.into_iter().map(f).collect()},
    )
}

pub fn iso_option<A: 'static, B: 'static>((f, g): ISO<A, B>) -> ISO<Option<A>, Option<B>> {
    iso(
        move |v| match v { None => None, Some(x) => Some(f(x)) },
        move |v| match v { None => None, Some(x) => Some(g(x)) }
    )
}

pub fn iso_result<A, B, C, D>((f_ab, g_ab): ISO<A, B>, (f_cd, g_cd): ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>>
    where A: 'static, B: 'static, C: 'static, D: 'static {
    iso(
        move |v| match v { Ok(v) => Ok(f_ab(v)), Err(e) => Err(f_cd(e)) },
        move |v| match v { Ok(v) => Ok(g_ab(v)), Err(e) => Err(g_cd(e)) },
    )
}

/// Going another way is hard (and is generally impossible)
/// Remember, for all valid ISO, converting and converting back
/// is the same as the original value.
/// You need this to prove some case are impossible.
pub fn iso_un_option<A: 'static, B: 'static>((f, g): ISO<Option<A>, Option<B>>) -> ISO<A, B> {
    iso(
        move |v| match f(Some(v)) {Some(x) => x, None => f(None).unwrap()},
        move |v| match g(Some(v)) {Some(x) => x, None => g(None).unwrap()},
    )
}

/// inf + 0 = inf + 1
pub fn iso_eu() -> ISO<Result<Vec<()>, ()>, Result<Vec<()>, Void>> {
    fn f(r: Result<Vec<()>, ()>) -> Result<Vec<()>, Void> {
        match r {
            Ok(v) => Ok([v, vec![()]].concat()),
            Err(_) => Ok(Vec::new())
        }
    }

    fn g(r: Result<Vec<()>, Void>) -> Result<Vec<()>, ()> {
        match r {
            Ok(v) => if v.is_empty() {Err(())} else {Ok(Vec::from(&v[..(v.len()-1)]))},
            Err(e) => absurd(e)
        }
    }

    iso(f, g)
}

pub type IsoFL<A, B, C, D> = Box<dyn FnOnce(Box<dyn Fn(A) -> C>) -> Box<dyn FnOnce(B) -> D>>;
pub type IsoFR<A, B, C, D> = Box<dyn FnOnce(Box<dyn Fn(B) -> D>) -> Box<dyn FnOnce(A) -> C>>;
pub type IsoF<A, B, C, D> = (IsoFL<A, B, C, D>, IsoFR<A, B, C, D>);

/// translator note:
/// FnBox is not yet supported, we can only return an uncallable
/// Box<FnOnce> (RetFunc). You should return the function with
/// correct type, which will be checked by the tests.
/// The type annotation is shown above. You need you return something like
/// (Box::new(...), Box::new(...))
pub fn iso_func<A, B, C, D>((f_ab, g_ab): ISO<A, B>, (f_cd, g_cd): ISO<C, D>) -> IsoF<A, B, C, D>
    where A: 'static, B: 'static, C: 'static, D: 'static {
    (
        Box::new(|h| Box::new(move |x| f_cd(h(g_ab(x))))),
        Box::new(|h| Box::new(move |x| g_cd(h(f_ab(x))))),
    )
}

/// And we have isomorphism on isomorphism!
pub fn iso_symm<A: 'static, B: 'static>() -> ISO<ISO<A, B>, ISO<B, A>> {
    iso(symm, symm)
}

/// Sometimes, we can treat a Type as a Number:
/// if a Type t has n distinct value, it's Number is n.
/// This is formally called cardinality.
/// See https://en.wikipedia.org/wiki/Cardinality
///
/// Void has cardinality of 0 (we will abbreviate it Void is 0).
/// () is 1.
/// Bool is 2.
/// Maybe a is 1 + a.
/// We will be using peano arithmetic so we will write it as S a.
/// https://en.wikipedia.org/wiki/Peano_axioms
/// Either a b is a + b.
/// (a, b) is a * b.
/// a => b is b ^ a. Try counting (() => Bool) and (Bool => ())
///
/// Algebraic data type got the name because
/// it satisfies a lot of algebraic rules under isomorphism

/// a = b => c = d => a * c = b * d
pub fn iso_prod<A, B, C, D>(ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<(A, C), (B, D)>
    where A: 'static, B: 'static, C: 'static, D: 'static {
    iso_tuple(ab, cd)
}

/// a = b => c = d => a + c = b + d
pub fn iso_plus<A, B, C, D>(ab: ISO<A, B>, cd: ISO<C, D>) -> ISO<Result<A, C>, Result<B, D>>
    where A: 'static, B: 'static, C: 'static, D: 'static {
    iso_result(ab, cd)
}

/// a = b => S a = S b
pub fn iso_s<A: 'static, B: 'static>(i: ISO<A, B>) -> ISO<Option<A>, Option<B>> {
    iso_option(i)
}

/// a = b => c = d => c ^ a = d ^ b
pub fn iso_pow<A: 'static, B: 'static, C: 'static, D: 'static>(ab: ISO<A, B>, cd: ISO<C, D>) -> IsoF<A, B, C, D> {
    iso_func(ab, cd)
}

/// a + b = b + a
pub fn plus_comm<A: 'static, B: 'static>() -> ISO<Result<A, B>, Result<B, A>> {
    fn f<X: 'static, Y: 'static>(v: Result<X, Y>) -> Result<Y, X> { match v {Ok(x) => Err(x), Err(y) => Ok(y) } }

    iso(f, f)
}

/// a + b + c = a + (b + c)
pub fn plus_assoc<A: 'static, B: 'static, C: 'static>() -> ISO<Result<Result<A, B>, C>, Result<A, Result<B, C>>> {
    fn f<X, Y, Z>(v: Result<Result<X, Y>, Z>) -> Result<X, Result<Y, Z>>
        where X: 'static, Y: 'static, Z: 'static {
        match v {
            Ok(r) => match r { Ok(x) => Ok(x), Err(y) => Err(Ok(y)) }
            Err(z) => Err(Err(z))
        }
    }

    fn g<X, Y, Z>(v: Result<X, Result<Y, Z>>) -> Result<Result<X, Y>, Z>
        where X: 'static, Y: 'static, Z: 'static {
        match v {
            Ok(x) => Ok(Ok(x)),
            Err(r) => match r { Ok(y) => Ok(Err(y)), Err(z) => Err(z) }
        }
    }

    iso(f, g)
}

/// a * b = b * a
pub fn mult_comm<A: 'static, B: 'static>() -> ISO<(A, B), (B, A)> {
    fn f<X: 'static, Y: 'static>(v: (X, Y)) -> (Y, X) { (v.1, v.0) }

    iso(f, f)
}

/// a * b * c = a * (b * c)
pub fn mult_assoc<A: 'static, B: 'static, C: 'static>() -> ISO<((A, B), C), (A, (B, C))> {
    iso(move |((a, b), c)| (a, (b, c)), move |(a, (b, c))| ((a, b), c))
}

/// a * (b + c) = a * b + a * c
pub fn dist<A: 'static, B: 'static, C: 'static>() -> ISO<(A, Result<B, C>), Result<(A, B), (A, C)>> {
    fn f<X, Y, Z>(v: (X, Result<Y, Z>)) -> Result<(X, Y), (X, Z)>
        where X: 'static, Y: 'static, Z: 'static {
        match v.1 {
            Ok(y) => Ok((v.0, y)),
            Err(z) => Err((v.0, z)),
        }
    }

    fn g<X, Y, Z>(v: Result<(X, Y), (X, Z)>) -> (X, Result<Y, Z>)
        where X: 'static, Y: 'static, Z: 'static {
        match v {
            Ok(r) => (r.0, Ok(r.1)),
            Err(e) => (e.0, Err(e.1)),
        }
    }

    iso(f, g)
}

pub type IsoCL<A, B, C> = RetFunc<Func<A, Func<B, C>>, RetFunc<(A, B), C>>;
pub type IsoCR<A, B, C> = RetFunc<Func<(A, B), C>, RetFunc<A, RetFunc<B, C>>>;
pub type IsoC<A, B, C> = (IsoCL<A, B, C>, IsoCR<A, B, C>);

/// translator note:
/// FnBox is not yet supported, we can only return an uncallable
/// Box<FnOnce> (RetFunc). You should return the function with
/// correct type, which will be checked by the tests.
/// later you'll have to implement three more functions that related
/// to `RetFunc`. enjoy!

/// (c ^ b) ^ a = c ^ (a * b)
pub fn curry_iso<A: 'static, B: 'static, C: 'static>() -> IsoC<A, B, C> {
    (
        Box::new(|v| Box::new(move |(a, b)| v(a)(b))),
        Box::new(|v| Box::new(|a| Box::new(move |b| v((a, b))))),
    )
}

/// 1 = S O (we are using peano arithmetic)
/// https://en.wikipedia.org/wiki/Peano_axioms
pub fn one() -> ISO<(), Option<Void>> {
    iso(|x| None, |x| ())
}

/// 2 = S (S O)
pub fn two() -> ISO<bool, Option<Option<Void>>> {
    iso(|x| if x {Some(None)} else {None}, |x| match x {Some(_) => true, None => false})
}

/// 0 + b = b
pub fn plus_o<B: 'static>() -> ISO<Result<Void, B>, B> {
    iso(
        |x| match x {Ok(z) => absurd(z), Err(e) => e},
        |x| Err(x),
    )
}

/// S a + b = S (a + b)
pub fn plus_s<A: 'static, B: 'static>() -> ISO<Result<Option<A>, B>, Option<Result<A, B>>> {
    iso(
        |x| match x {
            Ok(o) => match o {
                Some(a) => Some(Ok(a)),
                None => None,
            },
            Err(b) => Some(Err(b)),
        },
        |x| match x {
            Some(r) => match r {
                Ok(a) => Ok(Some(a)),
                Err(b) => Err(b),
            },
            None => Ok(None),
        }
    )
}

/// 1 + b = S b
pub fn plus_so<B: 'static>() -> ISO<Result<(), B>, Option<B>> {
    trans(
        iso_plus(one(), refl()),
        trans(plus_s(), iso_s(plus_o())),
    )
}

/// 0 * a = 0
pub fn mult_o<A: 'static>() -> ISO<(Void, A), Void> {
    iso(
        |(a, b)| a,
        |v| absurd(v),
    )
}

/// S a * b = b + a * b
pub fn mult_s<A: 'static, B: 'static>() -> ISO<(Option<A>, B), Result<B, (A, B)>> {
    iso(
        |(x, b)| match x {
            Some(a) => Err((a, b)),
            None => Ok(b),
        },
        |r| match r {
            Ok(b) => (None, b),
            Err((a, b)) => (Some(a), b),
        },
    )
}

/// 1 * b = b
pub fn mult_so<B: 'static>() -> ISO<((), B), B> {
    trans(iso_prod(one(), refl()),
          trans(mult_s(),
                trans(iso_plus(refl(), mult_o()),
                      trans(plus_comm(), plus_o()))))
}

/// Here we go, the last three functions related to
/// RetFunc. They're easy!

pub type IsoPL<A> = RetFunc<Func<Void, A>, ()>;
pub type IsoPR<A> = RetFunc<(), RetFunc<Void, A>>;
pub type IsoP<A> = (IsoPL<A>, IsoPR<A>);

/// a ^ 0 = 1
pub fn pow_o<A: 'static>() -> IsoP<A> {
    (
        Box::new(|x| ()),
        Box::new(|_x| Box::new(|x| absurd(x))),
    )
}

pub type IsoPsL<A, B> = RetFunc<Func<Option<B>, A>, (A, RetFunc<B, A>)>;
pub type IsoPsR<A, B> = RetFunc<(A, Func<B, A>), RetFunc<Option<B>, A>>;
pub type IsoPs<A, B> = (IsoPsL<A, B>, IsoPsR<A, B>);

/// a ^ (S b) = a * (a ^ b)
pub fn pow_s<A: 'static, B: 'static>() -> IsoPs<A, B> {
    (
        Box::new(|f| (f(None), Box::new(move |b| f(Some(b))))),
        Box::new(|(a, f)| Box::new(move |o| match o {
            Some(b) => f(b),
            None => a,
        })),
    )
}

pub type IsoPsoL<A> = RetFunc<Func<(), A>, A>;
pub type IsoPsoR<A> = RetFunc<A, RetFunc<(), A>>;
pub type IsoPso<A> = (IsoPsoL<A>, IsoPsoR<A>);

/// a ^ 1 = a
/// In Haskell/Java/Dart, you can go the hard way
/// (like mult_so, plus_so) to prove that you really get what is
/// going on.
/// Unfortunately, in Rust, you can only go the trivial way.
/// Because Rust doesn't support FnBox ATM.
pub fn pow_so<A: 'static>() -> IsoPso<A> {
    (
        Box::new(|f| f(())),
        Box::new(|a| Box::new(move |_| a)),
    )
}
