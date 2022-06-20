59243a9825ac8e993e000060



using System;
using System.Linq;

namespace Kata
{
    public class CombatSimulator
    {
        private int _pcHitPoints;
        private readonly int _pcDefense;
        private int _enemyHitPoints;
        private readonly int _enemyDefense;

        public enum HitResult
        {
            FightOn,
            PcDead,
            EnemyDead
        }

        public CombatSimulator(int pcHitPoints, int pcDefense, int enemyHitPoints, int enemyDefense)
        {
            _pcHitPoints = pcHitPoints;
            _pcDefense = pcDefense;
            _enemyHitPoints = enemyHitPoints;
            _enemyDefense = enemyDefense;
        }

        private int CalculateDamge(int attackRoll, int[] modifiers) 
        => attackRoll + modifiers?.Sum() ?? 0;

        public HitResult PcAttack(int attackRoll, int[] modifiers, int damage)
        {
            if (CalculateDamge(attackRoll, modifiers) >= _enemyDefense)
                _enemyHitPoints -= damage;

            return _enemyHitPoints <= 0 
                ? HitResult.EnemyDead
                : HitResult.FightOn;
        }

        public HitResult EnemyAttack(int attackRoll, int[] modifiers, int damage)
        {
            if (CalculateDamge(attackRoll, modifiers) >= _pcDefense)
                _pcHitPoints -= damage;

            return _pcHitPoints <= 0
                ? HitResult.PcDead
                : HitResult.FightOn;
        }
    }
}
______________________________
using System;
using System.Linq;

namespace Kata
{
  public class CombatSimulator
  {  
    private Player m_pcPlayer;
    private Player m_enemyPlayer;
  
    public CombatSimulator(int pcHitPoints, int pcDefense, int enemyHitPoints, int enemyDefense)
    {
      m_pcPlayer = new Player(pcHitPoints, pcDefense, HitResult.PcDead);
      m_enemyPlayer = new Player(enemyHitPoints, enemyDefense, HitResult.EnemyDead);
    }

    public HitResult PcAttack(int attackRoll, int[] modifiers, int damage)
      => performAttack(new Attack(attackRoll, modifiers, damage), m_enemyPlayer);

    public HitResult EnemyAttack(int attackRoll, int[] modifiers, int damage)
      => performAttack(new Attack(attackRoll, modifiers, damage), m_pcPlayer);
    
    private HitResult performAttack(Attack attack, Player target)
    {
      var roll = attack.Roll + attack.Modifiers?.Sum();
      if(roll > target.Defense)
        target.HitPoints -= attack.Damage;
        
      if(target.HitPoints <= 0)
        return target.LostResult;
        
      return HitResult.FightOn;
    }
    
    public enum HitResult
    {
      FightOn,
      PcDead,
      EnemyDead
    }
  }
    
  public class Player
  {
    public int HitPoints { get; set; }
    public int Defense { get; set; }
    public CombatSimulator.HitResult LostResult { get; set; }
    
    public Player(int hitPoints, int defense, CombatSimulator.HitResult lostResult)
    {
      HitPoints = hitPoints;
      Defense = defense;
      LostResult = lostResult;
    }
  }
  
  public class Attack
  {
    public int Roll { get; set; }
    public int[] Modifiers { get; set; }
    public int Damage { get; set; }
    
    public Attack(int roll, int[] modifiers, int damage)
    {
      Roll = roll;
      Modifiers = modifiers;
      Damage = damage;
    }
  }
}
______________________________
using System;
using System.Linq;

namespace Kata
{
  public class CombatSimulator
  {
    public int pcHP;
    public int pcDefense;
    public int enemyHP;
    public int enemyDefense;
    
    public enum HitResult
    {
      FightOn,
      PcDead,
      EnemyDead
    }

    public CombatSimulator(int pcHP, int pcDefense, int enemyHP, int enemyDefense)
    {
      this.pcHP = pcHP;
      this.pcDefense = pcDefense;
      this.enemyHP = enemyHP;
      this.enemyDefense = enemyDefense;
    }

    public HitResult PcAttack(int attackRoll, int[] modifiers, int damage)
    {
      this.enemyHP -= attackRoll + (modifiers == null ? 0 : modifiers.Sum()) > this.enemyDefense ? damage : 0;
      return this.enemyHP <= 0 ? HitResult.EnemyDead : HitResult.FightOn;
    }

    public HitResult EnemyAttack(int attackRoll, int[] modifiers, int damage)
    {
      this.pcHP -= attackRoll + (modifiers == null ? 0 : modifiers.Sum()) > this.pcDefense ? damage : 0;
      return this.pcHP <= 0 ? HitResult.PcDead : HitResult.FightOn;
    }
  }
}
______________________________
using System;
using System.Linq;

namespace Kata
{
  public class CombatSimulator
  {
    public enum HitResult
    {
      FightOn,
      PcDead,
      EnemyDead
    }

    int _pcHP = 0;
    int _pcDef = 0;
    int _enemyHP = 0;
    int _enemyDef = 0;
    
    public CombatSimulator(int pcHitPoints, int pcDefense, int enemyHitPoints, int enemyDefense)
    {
      _pcHP = pcHitPoints;
      _pcDef = pcDefense;
      _enemyHP = enemyHitPoints;
      _enemyDef = enemyDefense;
    }

    public HitResult PcAttack(int attackRoll, int[] modifiers, int damage)
    {
      if (attackRoll + (modifiers == null ? 0 : modifiers.Sum()) > _enemyDef)
        _enemyHP -= damage;
    
      return (_enemyHP >= 0 ? HitResult.FightOn : HitResult.EnemyDead);
    }

    public HitResult EnemyAttack(int attackRoll, int[] modifiers, int damage)
    {
      if (attackRoll + (modifiers == null ? 0 : modifiers.Sum()) > _pcDef)
        _pcHP -= damage;
    
      return (_pcHP >= 0 ? HitResult.FightOn : HitResult.PcDead);
    }
  }
}
