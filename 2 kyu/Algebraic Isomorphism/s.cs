using System;
using System.Collections.Generic;
using System.Linq;

// ReSharper disable InconsistentNaming

public class Either
{
  public static Either<L, R> Left<L, R>(L l) => Either<L, R>.Left(l);
  public static Either<L, R> Right<L, R>(R r) => Either<L, R>.Right(r);
}

public abstract class Either<L, R>
{
  public abstract T Match<T>(Func<L, T> lf, Func<R, T> rf);
  public abstract Either<T, U> BiMap<T, U>(Func<L, T> lf, Func<R, U> rf);
  public abstract override bool Equals(object obj);
  public abstract override int GetHashCode();

  public static Either<L, R> Left(L l) => new _Left(l);
  public static Either<L, R> Right(R r) => new _Right(r);

  public class _Left : Either<L, R>
  {
    private readonly L l;

    public _Left(L l) =>
      this.l = l;

    public override T Match<T>(Func<L, T> lf, Func<R, T> rf) =>
      lf(l);

    public override Either<T, U> BiMap<T, U>(Func<L, T> lf, Func<R, U> rf) =>
      Either<T, U>.Left(lf(l));

    public override bool Equals(object obj) =>
      obj is _Left el && l.Equals(el.l);

    public override int GetHashCode() =>
      l.GetHashCode();
  }

  public class _Right : Either<L, R>
  {
    private readonly R r;

    public _Right(R r) =>
      this.r = r;

    public override T Match<T>(Func<L, T> lf, Func<R, T> rf) =>
      rf(r);

    public override Either<T, U> BiMap<T, U>(Func<L, T> lf, Func<R, U> rf) =>
      Either<T, U>.Right(rf(r));

    public override bool Equals(object obj) =>
      obj is _Right er && r.Equals(er.r);

    public override int GetHashCode() =>
      r.GetHashCode();
  }
}

public class Optional
{
  public static Optional<T> From<T>(T t) => Optional<T>.From(t);
  public static Optional<T> Empty<T>() => Optional<T>.Empty();
}

public abstract class Optional<T>
{
  public abstract Optional<R> Map<R>(Func<T, R> f);
  public abstract Optional<R> FlatMap<R>(Func<T, Optional<R>> f);
  public abstract T Get();
  public abstract T OrElseGet(Func<T> g);
  public abstract bool IsPresent();
  public abstract R Match<R>(Func<R> g, Func<T, R> f);
  public abstract override bool Equals(object obj);
  public abstract override int GetHashCode();

  public static Optional<T> From(T t) => new _From(t);
  public static Optional<T> Empty() => _Empty.INSTANCE;

  public class _From : Optional<T>
  {
    private readonly T t;

    public _From(T t) =>
      this.t = t;

    public override bool Equals(object obj) =>
      obj is _From os && t.Equals(os.t);

    public override int GetHashCode() =>
      t.GetHashCode();

    public override Optional<R> Map<R>(Func<T, R> f) =>
      Optional<R>.From(f(t));

    public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f) => f(t);
    public override T Get() => t;
    public override T OrElseGet(Func<T> g) => t;
    public override bool IsPresent() => true;
    public override R Match<R>(Func<R> g, Func<T, R> f) => f(t);
  }

  public class _Empty : Optional<T>
  {
    public static readonly _Empty INSTANCE = new _Empty();

    public override bool Equals(object obj) =>
      obj is _Empty;

    public override Optional<R> Map<R>(Func<T, R> f) =>
      Optional<R>.Empty();

    public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f) =>
      Optional<R>.Empty();

    public override T Get() =>
      throw new Exception("cannot get from Empty");

    public override T OrElseGet(Func<T> g) => g();
    public override bool IsPresent() => false;
    public override R Match<R>(Func<R> g, Func<T, R> f) => g();
    public override int GetHashCode() => 0;
  }
}

public abstract class Void
{
  public abstract A Absurd<A>();
}

public class Unit
{
  public static readonly Unit INSTANCE = new Unit();
}

public class ISO<A, B>
{
  public Func<A, B> Fw;
  public Func<B, A> Bw;

  public ISO(Func<A, B> fw, Func<B, A> bw)
  {
    Fw = fw;
    Bw = bw;
  }
}

public static class Isomorphism
{
  /// Fromtimes, we can treat a Type as a Number:
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

  public static ISO<A, B> Iso<A, B>(Func<A, B> fw, Func<B, A> bw) => new ISO<A, B>(fw, bw);
  public static Func<A, B> SubStL<A, B>(ISO<A, B> iso) => iso.Fw;
  public static Func<B, A> SubStR<A, B>(ISO<A, B> iso) => iso.Bw;

  public static ISO<A, A> Refl<A>() =>
    Iso<A, A>(a => a, a => a);

  public static ISO<B, A> Symm<A, B>(ISO<A, B> iso) =>
    Iso<B, A>(iso.Bw, iso.Fw);

  public static ISO<A, C> Trans<A, B, C>(ISO<A, B> ab, ISO<B, C> bc) =>
    Iso<A, C>(
      a => bc.Fw(ab.Fw(a)),
      c => ab.Bw(bc.Bw(c))
    );

  public static ISO<bool, bool> IsoBool() =>
    Refl<bool>();

  public static ISO<bool, bool> IsoBoolNot() =>
    Iso<bool, bool>(b => !b, b => !b);

  public static ISO<Tuple<A, C>, Tuple<B, D>> IsoTuple<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    Iso<Tuple<A, C>, Tuple<B, D>>(
      t => Tuple.Create(ab.Fw(t.Item1), cd.Fw(t.Item2)),
      t => Tuple.Create(ab.Bw(t.Item1), cd.Bw(t.Item2))
    );

  public static ISO<Either<A, C>, Either<B, D>> IsoEither<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    Iso<Either<A, C>, Either<B, D>>(
      e => e.BiMap(ab.Fw, cd.Fw),
      e => e.BiMap(ab.Bw, cd.Bw)
    );

  public static ISO<Optional<A>, Optional<B>> IsoOptional<A, B>(ISO<A, B> iso) =>
    Iso<Optional<A>, Optional<B>>(
      o => o.Map(iso.Fw),
      o => o.Map(iso.Bw)
    );

  public static ISO<A, B> IsoUnOptional<A, B>(ISO<Optional<A>, Optional<B>> iso) =>
    Iso<A, B>(
      a => iso.Fw(Optional.From(a)).OrElseGet(() => iso.Fw(Optional.Empty<A>()).Get()),
      b => iso.Bw(Optional.From(b)).OrElseGet(() => iso.Bw(Optional.Empty<B>()).Get())
    );

  public static ISO<List<A>, List<B>> IsoList<A, B>(ISO<A, B> iso) =>
    Iso<List<A>, List<B>>(
      l => l.Select(iso.Fw).ToList(),
      l => l.Select(iso.Bw).ToList()
    );

  public static ISO<Either<List<Unit>, Unit>, Either<List<Unit>, Void>> IsoEU() =>
    Iso<Either<List<Unit>, Unit>, Either<List<Unit>, Void>>(
      e =>
      {
        var s = e.Match(
          l =>
          {
            var i = new List<Unit>(l);
            i.Add(Unit.INSTANCE);
            return i;
          },
          u => new List<Unit>()
        );
        return Either.Left<List<Unit>, Void>(s);
      },
      e => e.Match(
        l =>
        {
          var c = l.Count;
          if (c == 0)
          {
            return Either.Right<List<Unit>, Unit>(Unit.INSTANCE);
          }
          var i = new List<Unit>(l);
          i.RemoveAt(c - 1);
          return Either.Left<List<Unit>, Unit>(i);
        },
        v => v.Absurd<Either<List<Unit>, Unit>>()
      )
    );

  public static ISO<ISO<A, B>, ISO<B, A>> IsoSymm<A, B>() =>
    Iso<ISO<A, B>, ISO<B, A>>(Symm, Symm);

  public static ISO<Func<A, C>, Func<B, D>> IsoFunc<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    Iso<Func<A, C>, Func<B, D>>(
      f => b => cd.Fw(f(ab.Bw(b))),
      f => a => cd.Bw(f(ab.Fw(a)))
    );

  /// a = b => c = d => a * c = b * d
  public static ISO<Tuple<A, C>, Tuple<B, D>> IsoProd<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    IsoTuple(ab, cd);

  /// a = b => c = d => a + c = b + d
  public static ISO<Either<A, C>, Either<B, D>> IsoPlus<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    IsoEither(ab, cd);

  /// a = b => S a = S b
  public static ISO<Optional<A>, Optional<B>> IsoS<A, B>(ISO<A, B> iso) =>
    IsoOptional(iso);

  /// a = b => c = d => c ^ a = d ^ b
  public static ISO<Func<A, C>, Func<B, D>> IsoPow<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    IsoFunc(ab, cd);

  /// a + b = b + a
  public static ISO<Either<A, B>, Either<B, A>> PlusComm<A, B>() =>
    Iso<Either<A, B>, Either<B, A>>(
      e => e.Match(
        a => Either.Right<B, A>(a),
        b => Either.Left<B, A>(b)
      ),
      e => e.Match(
        b => Either.Right<A, B>(b),
        a => Either.Left<A, B>(a)
      )
    );

  /// a + b + c = a + (b + c)
  public static ISO<Either<Either<A, B>, C>, Either<A, Either<B, C>>> PlusAssoc<A, B, C>() =>
    Iso<Either<Either<A, B>, C>, Either<A, Either<B, C>>>(
      e => e.Match(
        i => i.Match(
          a => Either.Left<A, Either<B, C>>(a),
          b => Either.Right<A, Either<B, C>>(Either.Left<B, C>(b))
        ),
        c => Either.Right<A, Either<B, C>>(Either.Right<B, C>(c))
      ),
      e => e.Match(
        a => Either.Left<Either<A, B>, C>(Either.Left<A, B>(a)),
        i => i.Match(
          b => Either.Left<Either<A, B>, C>(Either.Right<A, B>(b)),
          c => Either.Right<Either<A, B>, C>(c)
        )
      )
    );

  /// a * b = b * a
  public static ISO<Tuple<A, B>, Tuple<B, A>> MultComm<A, B>() =>
    Iso<Tuple<A, B>, Tuple<B, A>>(
      t => Tuple.Create(t.Item2, t.Item1),
      t => Tuple.Create(t.Item2, t.Item1)
    );

  /// a * b * c = a * (b * c)
  public static ISO<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>> PultAssoc<A, B, C>() =>
    Iso<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>>(
      t => Tuple.Create(t.Item1.Item1, Tuple.Create(t.Item1.Item2, t.Item2)),
      t => Tuple.Create(Tuple.Create(t.Item1, t.Item2.Item1), t.Item2.Item2)
    );

  /// a * (b + c) = a * b + a * c
  public static ISO<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>> Dist<A, B, C>() =>
    Iso<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>>(
      t => t.Item2.BiMap(
        b => Tuple.Create(t.Item1, b),
        c => Tuple.Create(t.Item1, c)
      ),
      e => e.Match(
        t => Tuple.Create(t.Item1, Either.Left<B, C>(t.Item2)),
        t => Tuple.Create(t.Item1, Either.Right<B, C>(t.Item2))
      )
    );

  /// (c ^ b) ^ a = c ^ (a * b)
  public static ISO<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>> CurryISO<A, B, C>() =>
    Iso<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>>(
      f => t => f(t.Item1)(t.Item2),
      f => a => b => f(Tuple.Create(a, b))
    );

  /// 1 = S 0 (we are using peano arithmetic)
  public static ISO<Unit, Optional<Void>> One() =>
    Iso<Unit, Optional<Void>>(
      u => Optional.Empty<Void>(),
      o => o.Match(() => Unit.INSTANCE, v => v.Absurd<Unit>())
    );

  /// 2 = S (S 0)
  public static ISO<bool, Optional<Optional<Void>>> Two() =>
    Iso<bool, Optional<Optional<Void>>>(
      b => b
        ? Optional.From(Optional.Empty<Void>())
        : Optional.Empty<Optional<Void>>(),
      o => o.IsPresent()
    );

  /// 0 + b = b
  public static ISO<Either<Void, B>, B> PlusO<B>() =>
    Iso<Either<Void, B>, B>(
      e => e.Match(v => v.Absurd<B>(), b => b),
      b => Either.Right<Void, B>(b)
    );

  /// S a + b = S (a + b)
  public static ISO<Either<Optional<A>, B>, Optional<Either<A, B>>> PlusS<A, B>() =>
    Iso<Either<Optional<A>, B>, Optional<Either<A, B>>>(
      e => e.Match(
        o => o.Map(a => Either.Left<A, B>(a)),
        b => Optional.From(Either.Right<A, B>(b))
      ),
      o => o.Match(
        () => Either.Left<Optional<A>, B>(Optional.Empty<A>()),
        e => e.BiMap(a => Optional.From(a), b => b)
      )
    );

  /// 1 + b = S b
  public static ISO<Either<Unit, B>, Optional<B>> PlusSO<B>() =>
    Trans(IsoPlus(One(), Refl<B>()),
      Trans(PlusS<Void, B>(), IsoS(PlusO<B>()))
    );

  /// 0 * a = 0
  public static ISO<Tuple<Void, A>, Void> MultO<A>() =>
    Iso<Tuple<Void, A>, Void>(
      t => t.Item1,
      v => Tuple.Create(v, v.Absurd<A>())
    );

  /// S a * b = b + a * b
  public static ISO<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>> MultS<A, B>() =>
    Iso<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>>(
      t => t.Item1.Match(
        () => Either.Left<B, Tuple<A, B>>(t.Item2),
        a => Either.Right<B, Tuple<A, B>>(Tuple.Create(a, t.Item2))
      ),
      e => e.Match(
        b => Tuple.Create(Optional.Empty<A>(), b),
        t => Tuple.Create(Optional.From(t.Item1), t.Item2)
      )
    );

  /// 1 * b = b
  public static ISO<Tuple<Unit, B>, B> MultSO<B>() =>
    Trans(IsoProd(One(), Refl<B>()),
      Trans(MultS<Void, B>(),
        Trans(IsoPlus(Refl<B>(), MultO<B>()),
          Trans(PlusComm<B, Void>(), PlusO<B>())
        )
      )
    );

  /// a ^ 0 = 1
  public static ISO<Func<Void, A>, Unit> PowO<A>() =>
    Iso<Func<Void, A>, Unit>(
      f => Unit.INSTANCE,
      u => v => v.Absurd<A>()
    );

  /// a ^ (S b) = a * (a ^ b)
  public static ISO<Func<Optional<B>, A>, Tuple<A, Func<B, A>>> PowS<A, B>() =>
    Iso<Func<Optional<B>, A>, Tuple<A, Func<B, A>>>(
      f => Tuple.Create<A, Func<B, A>>(f(Optional.Empty<B>()), b => f(Optional.From(b))),
      t => o => o.Match(() => t.Item1, b => t.Item2(b))
    );

  /// a ^ 1 = a
  public static ISO<Func<Unit, A>, A> PowSO<A>() =>
    Trans(IsoPow(One(), Refl<A>()),
      Trans(PowS<A, Void>(),
        Trans(IsoProd(Refl<A>(), PowO<A>()),
          Trans(MultComm<A, Unit>(), MultSO<A>())
        )
      )
    );

  public static ISO<Tuple<A, C>, Tuple<B, D>> isoProd<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    IsoTuple(ab, cd);
}
_______________________________________________________________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

// ReSharper disable InconsistentNaming
#pragma warning disable 693
#pragma warning disable 659

public abstract class Either<L, R> {
  
	public abstract T Match<T>(Func<L, T> lt, Func<R, T> rt);
	public abstract override bool Equals(object obj);
	public static Either<L, R> Left(L l) => new _Left<L, R>(l);
	public static Either<L, R> Right(R r) => new _Right<L, R>(r);

	public class _Left<L, R> : Either<L, R> {
		private readonly L l;
		public _Left(L l) => this.l = l;
		public override T Match<T>(Func<L, T> lt, Func<R, T> rt) => lt(l);
		public override bool Equals(object rhs) => rhs is Either<L, R>
			       && ((Either<L, R>) rhs).Match(arg => l.Equals(arg), rr => false);
	}

	public class _Right<L, R> : Either<L, R> {
		private readonly R r;
		public _Right(R r) => this.r = r;
		public override T Match<T>(Func<L, T> lt, Func<R, T> rt) => rt(r);
		public override bool Equals(object rhs) => rhs is Either<L, R>
			       && ((Either<L, R>) rhs).Match(ll => false, arg => r.Equals(arg));
	}
}

public abstract class Void {
	public abstract A Absurd<A>();
}

public class Unit {
	private Unit() {}
	public static readonly Unit INSTANCE = new Unit();
}

public abstract class Optional<T> {
  
	public static Optional<T> From(T obj) => new Some<T>(obj);
	public static Optional<T> Empty() => new None<T>();
	public abstract Optional<R> Map<R>(Func<T, R> f);
	public abstract Optional<R> FlatMap<R>(Func<T, Optional<R>> f);
	public abstract T Get();
	public abstract T OrElseGet(Func<T> f);
	public abstract bool IsPresent();
	public abstract override bool Equals(object obj);

	public class Some<T> : Optional<T> {
		private readonly T _obj;
		public Some(T obj) => _obj = obj;
		public override Optional<R> Map<R>(Func<T, R> f) => new Some<R>(f(_obj));
		public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f) => f(_obj);
		public override bool Equals(object other) => other is Some<T> && Equals(_obj, ((Some<T>) other)._obj);
		public override T Get() => _obj;
		public override T OrElseGet(Func<T> f) => _obj;
		public override bool IsPresent() => true;
	}

	public class None<T> : Optional<T> {
		public override Optional<R> Map<R>(Func<T, R> f) => new None<R>();
		public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f) => new None<R>();
		public override T Get() => throw new Exception("cannot get from null");
		public override bool Equals(object obj) => null != obj && obj.GetType().Name.Equals("None`1");
		public override T OrElseGet(Func<T> f) => f();
		public override bool IsPresent() => false;
	}
}

public class ISO<A, B> {
	public Func<A, B> Fw;
	public Func<B, A> Bw;
	public ISO(Func<A, B> fw, Func<B, A> bw) => (Fw, Bw) = (fw, bw);
}

public static class Isomorphism {

  // imports
  public static Func<A, B> SubStL<A, B>(ISO<A, B> iso) => iso.Fw;
  public static Func<B, A> SubStR<A, B>(ISO<A, B> iso) => iso.Bw;
  public static ISO<A, A> Refl<A>() => new ISO<A, A>(a => a, b => b);
  public static ISO<bool, bool> IsoBool() => Refl<bool>();
  public static ISO<bool, bool> IsoBoolNot() => new ISO<bool, bool>(a => !a, b => !b);
  public static ISO<A, B> Symm<A, B>(ISO<B, A> iso) => new ISO<A, B>(iso.Bw, iso.Fw);
  public static ISO<A, C> Trans<A, B, C>(ISO<A, B> ab, ISO<B, C> bc) => new ISO<A, C>(a => bc.Fw(ab.Fw(a)), c => ab.Bw(bc.Bw(c)));
  public static ISO<Tuple<A, C>, Tuple<B, D>> IsoTuple<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => new ISO<Tuple<A, C>, Tuple<B, D>>(
      ac => Tuple.Create(ab.Fw(ac.Item1), cd.Fw(ac.Item2)),
      bd => Tuple.Create(ab.Bw(bd.Item1), cd.Bw(bd.Item2)));
  public static ISO<Either<A, C>, Either<B, D>> IsoEither<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => new ISO<Either<A, C>, Either<B, D>>(
      l => l.Match(a => Either<B, D>.Left(ab.Fw(a)), c => Either<B, D>.Right(cd.Fw(c))),
      r => r.Match(b => Either<A, C>.Left(ab.Bw(b)), d => Either<A, C>.Right(cd.Bw(d))));
  public static ISO<List<A>, List<B>> IsoList<A, B>(ISO<A, B> iso) => new ISO<List<A>, List<B>>(a => a.ConvertAll(i => iso.Fw(i)), b => b.ConvertAll(i => iso.Bw(i)));
  public static ISO<Optional<A>, Optional<B>> IsoOptional<A, B>(ISO<A, B> iso) => new ISO<Optional<A>, Optional<B>>(a => a.Map(iso.Fw), b => b.Map(iso.Bw));
  public static ISO<Either<List<Unit>, Unit>, Either<List<Unit>, Void>> IsoEU() => new ISO<Either<List<Unit>, Unit>, Either<List<Unit>, Void>>(
      le => le.Match(
        l => { l.Insert(0, Unit.INSTANCE); return Either<List<Unit>, Void>.Left(l);  },
        r => Either<List<Unit>, Void>.Left(new List<Unit>())),
      re => re.Match(l => l.Count != 0
        ? Either<List<Unit>, Unit>.Left(l.Skip(1).ToList())
        : Either<List<Unit>, Unit>.Right(Unit.INSTANCE), r => r.Absurd<Either<List<Unit>, Unit>>()));
  public static ISO<A, B> IsoUnOptional<A, B>(ISO<Optional<A>, Optional<B>> iso) => new ISO<A, B>(
      a => iso.Fw(Optional<A>.From(a)).OrElseGet(() => iso.Fw(Optional<A>.Empty()).Get()),
      b => iso.Bw(Optional<B>.From(b)).OrElseGet(() => iso.Bw(Optional<B>.Empty()).Get()));
  public static ISO<Func<A, C>, Func<B, D>> IsoFunc<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => new ISO<Func<A, C>, Func<B, D>>(ac => a => cd.Fw(ac(ab.Bw(a))), bd => b => cd.Bw(bd(ab.Fw(b))));
  public static ISO<ISO<A, B>, ISO<B, A>> IsoSymm<A, B>() => new ISO<ISO<A, B>, ISO<B, A>>(Symm, Symm);

	// kata
	public static ISO<Tuple<A, C>, Tuple<B, D>> isoProd<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoTuple(ab, cd);
  public static ISO<Either<A, C>, Either<B, D>> IsoPlus<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoEither(ab, cd);
	public static ISO<Optional<A>, Optional<B>> IsoS<A, B>(ISO<A, B> iso) => IsoOptional(iso);
	public static ISO<Func<A, C>, Func<B, D>> IsoPow<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoFunc(ab, cd);
	public static ISO<Either<L, R>, Either<R, L>> PlusComm<L, R>() => new ISO<Either<L, R>, Either<R, L>>(
      lr => lr.Match(Either<R, L>.Right, Either<R, L>.Left),
      rl => rl.Match(Either<L, R>.Right, Either<L, R>.Left));
  public static ISO<Either<Either<A, B>, C>, Either<A, Either<B, C>>> PlusAssoc<A, B, C>() => new ISO<Either<Either<A, B>, C>, Either<A, Either<B, C>>>(
      ls => ls.Match(ab => ab.Match(
          Either<A, Either<B, C>>.Left,
          b => Either<A, Either<B, C>>.Right(Either<B, C>.Left(b))),
          c => Either<A, Either<B, C>>.Right(Either<B, C>.Right(c))),
      ls => ls.Match(
          a => Either<Either<A, B>, C>.Left(Either<A, B>.Left(a)),
          bc => bc.Match(b => Either<Either<A, B>, C>.Left(Either<A, B>.Right(b)),
          Either<Either<A, B>, C>.Right)));
  public static ISO<Tuple<A, B>, Tuple<B, A>> MultComm<A, B>() => new ISO<Tuple<A, B>, Tuple<B, A>>(ab => Tuple.Create(ab.Item2, ab.Item1),
      t => Tuple.Create(t.Item2, t.Item1));
  public static ISO<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>> PultAssoc<A, B, C>() => new ISO<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>>(
      a => Tuple.Create(a.Item1.Item1, Tuple.Create(a.Item1.Item2, a.Item2)),
      b => Tuple.Create(Tuple.Create(b.Item1, b.Item2.Item1), b.Item2.Item2));
  public static ISO<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>> Dist<A, B, C>() => new ISO<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>>(
      ls => ls.Item2.Match(
        b => Either<Tuple<A, B>, Tuple<A, C>>.Left(Tuple.Create(ls.Item1, b)),
        c => Either<Tuple<A, B>, Tuple<A, C>>.Right(Tuple.Create(ls.Item1, c))),
      ls => ls.Match(
        a => Tuple.Create(a.Item1, Either<B, C>.Left(a.Item2)),
        b => Tuple.Create(b.Item1, Either<B, C>.Right(b.Item2))));
	public static ISO<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>> CurryISO<A, B, C>() => new ISO<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>>(
      a => t => a(t.Item1)(t.Item2),
      t => a => b => t(Tuple.Create(a, b)));
	public static ISO<Unit, Optional<Void>> One() => new ISO<Unit, Optional<Void>>(_ => Optional<Void>.Empty(), _ => Unit.INSTANCE);
	public static ISO<bool, Optional<Optional<Void>>> Two() => new ISO<bool, Optional<Optional<Void>>>(
      b => b ? Optional<Optional<Void>>.From(Optional<Void>.Empty()) : Optional<Optional<Void>>.Empty(),
      option => option.IsPresent());
	public static ISO<Either<Void, B>, B> PlusO<B>() => new ISO<Either<Void, B>, B>(vb => vb.Match(v => v.Absurd<B>(), b => b), Either<Void, B>.Right);
	public static ISO<Either<Optional<A>, B>, Optional<Either<A, B>>> PlusS<A, B>() => new ISO<Either<Optional<A>, B>, Optional<Either<A, B>>>(
      ls => ls.Match(oa => oa.Map(a => Optional<Either<A, B>>.From(Either<A, B>.Left(a))).OrElseGet(Optional<Either<A, B>>.Empty), b => Optional<Either<A, B>>.From(Either<A, B>.Right(b))),
      ls => ls.Map(ab => ab.Match(a => Either<Optional<A>, B>.Left(Optional<A>.From(a)), Either<Optional<A>, B>.Right)).OrElseGet(() => Either<Optional<A>, B>.Left(Optional<A>.Empty())));
	public static ISO<Either<Unit, B>, Optional<B>> PlusSO<B>() => Trans(IsoPlus(One(), Refl<B>()), Trans(PlusS<Void, B>(), IsoS(PlusO<B>())));
	public static ISO<Tuple<Void, A>, Void> MultO<A>() => new ISO<Tuple<Void, A>, Void>(a => a.Item1, v => v.Absurd<Tuple<Void, A>>());
	public static ISO<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>> MultS<A, B>() => new ISO<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>>(
      ls => ls.Item1.Map(a => Either<B, Tuple<A, B>>.Right(Tuple.Create(a, ls.Item2))) .OrElseGet(() => Either<B, Tuple<A, B>>.Left(ls.Item2)),
      ls => ls.Match(b => Tuple.Create(Optional<A>.Empty(), b), t => Tuple.Create(Optional<A>.From(t.Item1), t.Item2)));
	public static ISO<Tuple<Unit, B>, B> MultSO<B>() => Trans(isoProd(One(), Refl<B>()), Trans(MultS<Void, B>(),
      Trans(IsoPlus(Refl<B>(), MultO<B>()), Trans(PlusComm<B, Void>(), PlusO<B>()))));
	public static ISO<Func<Void, A>, Unit> PowO<A>() => new ISO<Func<Void, A>, Unit>(_ => Unit.INSTANCE, _ => v => v.Absurd<A>());
	public static ISO<Func<Optional<B>, A>, Tuple<A, Func<B, A>>> PowS<A, B>() => new ISO<Func<Optional<B>, A>, Tuple<A, Func<B, A>>>(
      f => Tuple.Create<A, Func<B, A>>(f(Optional<B>.Empty()), o => f(Optional<B>.From(o))),
      t => b => b.Map(t.Item2).OrElseGet(() => t.Item1));
	public static ISO<Func<Unit, A>, A> PowSO<A>() => Trans(IsoPow(One(), Refl<A>()), Trans(PowS<A, Void>(),
      Trans(isoProd(Refl<A>(), PowO<A>()), Trans(MultComm<A, Unit>(), MultSO<A>()))));
}
____________________________________________________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

// ReSharper disable InconsistentNaming
#pragma warning disable 693
#pragma warning disable 659

public abstract class Either<L, R>
{
  public abstract T Match<T>(Func<L, T> lt, Func<R, T> rt);
  public abstract override bool Equals(object obj);

  public static Either<L, R> Left(L l)
  {
    return new _Left<L, R>(l);
  }

  public static Either<L, R> Right(R r)
  {
    return new _Right<L, R>(r);
  }

  public class _Left<L, R> : Either<L, R>
  {
    private readonly L l;

    public _Left(L l)
    {
      this.l = l;
    }

    public override T Match<T>(Func<L, T> lt, Func<R, T> rt)
    {
      return lt(l);
    }

    public override bool Equals(object rhs)
    {
      return rhs is Either<L, R>
             && ((Either<L, R>) rhs).Match(arg => l.Equals(arg), rr => false);
    }
  }

  public class _Right<L, R> : Either<L, R>
  {
    private readonly R r;

    public _Right(R r)
    {
      this.r = r;
    }

    public override T Match<T>(Func<L, T> lt, Func<R, T> rt)
    {
      return rt(r);
    }

    public override bool Equals(object rhs)
    {
      return rhs is Either<L, R>
             && ((Either<L, R>) rhs).Match(ll => false, arg => r.Equals(arg));
    }
  }
}

public abstract class Void
{
  public abstract A Absurd<A>();
}

public class Unit
{
  private Unit()
  {
  }

  public static readonly Unit INSTANCE = new Unit();
}

/// <summary>
/// If there's a problem of variance,
/// the test will extract the value and compare.
/// </summary>
/// <typeparam name="T"></typeparam>
public abstract class Optional<T>
{
  public static Optional<T> From(T obj)
  {
    return new Some<T>(obj);
  }

  public static Optional<T> Empty()
  {
    return new None<T>();
  }

  public abstract R Match<R>(R r, Func<T, R> f);
  public abstract Optional<R> Map<R>(Func<T, R> f);
  public abstract Optional<R> FlatMap<R>(Func<T, Optional<R>> f);
  public abstract T Get();
  public abstract T OrElseGet(Func<T> f);
  public abstract bool IsPresent();
  public abstract override bool Equals(object obj);

  public class Some<T> : Optional<T>
  {
    private readonly T _obj;

    public Some(T obj)
    {
      _obj = obj;
    }

    public override R Match<R>(R r, Func<T, R> f) => f(_obj);

    public override Optional<R> Map<R>(Func<T, R> f)
    {
      return new Some<R>(f(_obj));
    }

    public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f)
    {
      return f(_obj);
    }

    public override bool Equals(object other)
    {
      return other is Some<T> && Equals(_obj, ((Some<T>) other)._obj);
    }

    public override T Get()
    {
      return _obj;
    }

    public override T OrElseGet(Func<T> f)
    {
      return _obj;
    }

    public override bool IsPresent()
    {
      return true;
    }
  }

  public class None<T> : Optional<T>
  {
    public override R Match<R>(R r, Func<T, R> f) => r;

    public override Optional<R> Map<R>(Func<T, R> f)
    {
      return new None<R>();
    }

    public override Optional<R> FlatMap<R>(Func<T, Optional<R>> f)
    {
      return new None<R>();
    }

    /// don't change this
    public override T Get()
    {
      throw new Exception("cannot get from null");
    }

    /// <summary>
    /// don't change this
    /// </summary>
    /// <param name="obj">other object</param>
    /// <returns>is equaled</returns>
    public override bool Equals(object obj)
    {
      return null != obj && obj.GetType().Name.Equals("None`1");
    }

    public override T OrElseGet(Func<T> f)
    {
      return f();
    }

    public override bool IsPresent()
    {
      return false;
    }
  }
}

public class ISO<A, B>
{
  public Func<A, B> Fw;
  public Func<B, A> Bw;

  public ISO(Func<A, B> fw, Func<B, A> bw)
  {
    Fw = fw;
    Bw = bw;
  }
}

public static class Isomorphism
{
  public static Func<A, B> SubStL<A, B>(ISO<A, B> iso) => iso.Fw;
  public static Func<B, A> SubStR<A, B>(ISO<A, B> iso) => iso.Bw;

  public static ISO<A, A> Refl<A>() => new ISO<A, A>(a => a, a => a);
  public static ISO<A, B> Symm<A, B>(ISO<B, A> iso) => new ISO<A, B>(iso.Bw, iso.Fw);
  public static ISO<A, C> Trans<A, B, C>(ISO<A, B> ab, ISO<B, C> bc) => new ISO<A, C>(a => bc.Fw(ab.Fw(a)), c => ab.Bw(bc.Bw(c)));

  public static ISO<bool, bool> IsoBool() => Refl<bool>();
  public static ISO<bool, bool> IsoBoolNot() => new ISO<bool, bool>(a => !a, a => !a);

  public static ISO<Tuple<A, C>, Tuple<B, D>> IsoTuple<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    new ISO<Tuple<A, C>, Tuple<B, D>>
      (t => new Tuple<B, D>(ab.Fw(t.Item1), cd.Fw(t.Item2)),
       t => new Tuple<A, C>(ab.Bw(t.Item1), cd.Bw(t.Item2)));

  public static ISO<Either<A, C>, Either<B, D>> IsoEither<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    new ISO<Either<A, C>, Either<B, D>>
      (eac => eac.Match<Either<B, D>>(a => Either<B, D>.Left(ab.Fw(a)), c => Either<B, D>.Right(cd.Fw(c))),
       ebd => ebd.Match<Either<A, C>>(b => Either<A, C>.Left(ab.Bw(b)), d => Either<A, C>.Right(cd.Bw(d))));
  
  public static ISO<Optional<A>, Optional<B>> IsoOptional<A, B>(ISO<A, B> iso) => 
    new ISO<Optional<A>, Optional<B>>(x => x.Map(iso.Fw), y => y.Map(iso.Bw));

  public static ISO<List<A>, List<B>> IsoList<A, B>(ISO<A, B> iso) =>
    new ISO<List<A>, List<B>>(s => s.ConvertAll(a => iso.Fw(a)), s => s.ConvertAll(a => iso.Bw(a)));

  public static ISO<Func<A, C>, Func<B, D>> IsoFunc<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) =>
    new ISO<Func<A, C>, Func<B, D>>(f => (b => cd.Fw(f(ab.Bw(b)))),
                                    g => (a => cd.Bw(g(ab.Fw(a)))));

  public static ISO<A, B> IsoUnOptional<A, B>(ISO<Optional<A>, Optional<B>> iso) =>
    new ISO<A, B>(a => iso.Fw(Optional<A>.From(a)).OrElseGet(() => iso.Fw(Optional<A>.Empty()).Get()), 
                  b => iso.Bw(Optional<B>.From(b)).OrElseGet(() => iso.Bw(Optional<B>.Empty()).Get()));

  public static ISO<ISO<A, B>, ISO<B, A>> IsoSymm<A, B>() =>
    new ISO<ISO<A, B>, ISO<B, A>>(Symm, Symm);

  /// a = b => c = d => a * c = b * d
  public static ISO<Tuple<A, C>, Tuple<B, D>> isoProd<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoTuple(ab, cd);
  /// a = b => c = d => a + c = b + d
  public static ISO<Either<A, C>, Either<B, D>> IsoPlus<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoEither(ab, cd);
  /// a = b => S a = S b
  public static ISO<Optional<A>, Optional<B>> IsoS<A, B>(ISO<A, B> iso) => IsoOptional(iso);
  /// a = b => c = d => c ^ a = d ^ b
  public static ISO<Func<A, C>, Func<B, D>> IsoPow<A, B, C, D>(ISO<A, B> ab, ISO<C, D> cd) => IsoFunc(ab, cd);
  /// a + b = b + a
  public static ISO<Either<L, R>, Either<R, L>> PlusComm<L, R>() =>
    new ISO<Either<L, R>, Either<R, L>>
      (lr => lr.Match(l => Either<R, L>.Right(l), r => Either<R, L>.Left(r)),
       rl => rl.Match(r => Either<L, R>.Right(r), l => Either<L, R>.Left(l)));
  /// a + b + c = a + (b + c)
  public static ISO<Either<Either<A, B>, C>, Either<A, Either<B, C>>> PlusAssoc<A, B, C>() =>
    new ISO<Either<Either<A, B>, C>, Either<A, Either<B, C>>>
      (abc => abc.Match(ab => ab.Match(a => Either<A, Either<B, C>>.Left(a), 
                                       b => Either<A, Either<B, C>>.Right(Either<B, C>.Left(b))),
                        c  => Either<A, Either<B, C>>.Right(Either<B, C>.Right(c))),
       abc => abc.Match(a  => Either<Either<A, B>, C>.Left(Either<A, B>.Left(a)),
                        bc => bc.Match(b => Either<Either<A, B>, C>.Left(Either<A, B>.Right(b)), 
                                       c => Either<Either<A, B>, C>.Right(c))));
                        
  /// a * b = b * a
  public static ISO<Tuple<A, B>, Tuple<B, A>> MultComm<A, B>() =>
    new ISO<Tuple<A, B>, Tuple<B, A>>
      (t => new Tuple<B, A>(t.Item2, t.Item1), 
       t => new Tuple<A, B>(t.Item2, t.Item1));

  /// a * b * c = a * (b * c)
  public static ISO<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>> PultAssoc<A, B, C>() =>
    new ISO<Tuple<Tuple<A, B>, C>, Tuple<A, Tuple<B, C>>>
      (t => new Tuple<A, Tuple<B, C>>(t.Item1.Item1, new Tuple<B, C>(t.Item1.Item2, t.Item2)),
       t => new Tuple<Tuple<A, B>, C>(new Tuple<A, B>(t.Item1, t.Item2.Item1), t.Item2.Item2));

  /// a * (b + c) = a * b + a * c
  public static ISO<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>> Dist<A, B, C>() =>
    new ISO<Tuple<A, Either<B, C>>, Either<Tuple<A, B>, Tuple<A, C>>>
      (abc => abc.Item2.Match(b => Either<Tuple<A, B>, Tuple<A, C>>.Left(new Tuple<A, B>(abc.Item1, b)),
                              c => Either<Tuple<A, B>, Tuple<A, C>>.Right(new Tuple<A, C>(abc.Item1, c))),
       abac => abac.Match(ab => new Tuple<A, Either<B, C>>(ab.Item1, Either<B, C>.Left(ab.Item2)),
                          ac => new Tuple<A, Either<B, C>>(ac.Item1, Either<B, C>.Right(ac.Item2))));
  
  /// (c ^ b) ^ a = c ^ (a * b)
  public static ISO<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>> CurryISO<A, B, C>() =>
    new ISO<Func<A, Func<B, C>>, Func<Tuple<A, B>, C>>
      (f => (ab => f(ab.Item1)(ab.Item2)),
       g => (a => (b => g(new Tuple<A, B>(a, b)))));


  /// 1 = S O (we are using peano arithmetic)
  public static ISO<Unit, Optional<Void>> One() =>
    new ISO<Unit, Optional<Void>>(_ => Optional<Void>.Empty(), _ => Unit.INSTANCE);

  /// 2 = S (S O)
  public static ISO<bool, Optional<Optional<Void>>> Two() =>
    new ISO<bool, Optional<Optional<Void>>>
      (b => b ? Optional<Optional<Void>>.From(Optional<Void>.Empty()) : Optional<Optional<Void>>.Empty(),
       o => o.IsPresent());

  /// 0 + b = b
  public static ISO<Either<Void, B>, B> PlusO<B>() =>
    new ISO<Either<Void, B>, B>
      (vbb => vbb.Match(v => v.Absurd<B>(), b => b),
       b => Either<Void, B>.Right(b));

  /// S a + b = S (a + b)
  public static ISO<Either<Optional<A>, B>, Optional<Either<A, B>>> PlusS<A, B>() =>
    new ISO<Either<Optional<A>, B>, Optional<Either<A, B>>>
      (ab => ab.Match(a => a.IsPresent() ? Optional<Either<A, B>>.From(Either<A, B>.Left(a.Get())) : Optional<Either<A, B>>.Empty(),
                      b => Optional<Either<A, B>>.From(Either<A, B>.Right(b))),
       ab => ab.IsPresent() ? ab.Get().Match(a => Either<Optional<A>, B>.Left(Optional<A>.From(a)), 
                                             b => Either<Optional<A>, B>.Right(b))
                            : Either<Optional<A>, B>.Left(Optional<A>.Empty()));
  /// 1 + b = S b
  public static ISO<Either<Unit, B>, Optional<B>> PlusSO<B>() =>
    Trans(IsoPlus(One(), Refl<B>()), Trans(PlusS<Void, B>(), IsoS(PlusO<B>())));

  /// 0 * a = 0
  public static ISO<Tuple<Void, A>, Void> MultO<A>() =>
    new ISO<Tuple<Void, A>, Void>(t => t.Item1, v => v.Absurd<Tuple<Void, A>>());

  /// S a * b = b + a * b
  public static ISO<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>> MultS<A, B>() =>
    new ISO<Tuple<Optional<A>, B>, Either<B, Tuple<A, B>>>
      (ab => ab.Item1.Match<Either<B, Tuple<A, B>>>(Either<B, Tuple<A, B>>.Left(ab.Item2),
                    a => Either<B, Tuple<A, B>>.Right(new Tuple<A, B>(a, ab.Item2))),
       bab => bab.Match(b => new Tuple<Optional<A>, B>(Optional<A>.Empty(), b),
                        ab => new Tuple<Optional<A>, B>(Optional<A>.From(ab.Item1), ab.Item2)));

  /// S 1 * b = b + 1 * b
  /// you simply have to complete the generic paramter
  public static ISO<Tuple<Unit, B>, B> MultSO<B>() =>
    new ISO<Tuple<Unit, B>, B>(ub => ub.Item2, b => new Tuple<Unit, B>(Unit.INSTANCE, b));

  /// a ^ 0 = 1
  public static ISO<Func<Void, A>, Unit> PowO<A>() =>
    new ISO<Func<Void, A>, Unit>(f => Unit.INSTANCE, _ => (v => v.Absurd<A>()));

  /// a ^ (S b) = a * (a ^ b)
  public static ISO<Func<Optional<B>, A>, Tuple<A, Func<B, A>>> PowS<A, B>() =>
    new ISO<Func<Optional<B>, A>, Tuple<A, Func<B, A>>>
      (f => new Tuple<A, Func<B, A>>(f(Optional<B>.Empty()), b => f(Optional<B>.From(b))),
       t => (b => b.Match(t.Item1, b => t.Item2(b))));

  /// a ^ 1 = a
  public static ISO<Func<Unit, A>, A> PowSO<A>() =>
    new ISO<Func<Unit, A>, A>(f => f(Unit.INSTANCE), a => (_ => a));
}
