54fe05c4762e2e3047000add


public class Ship
{
  public int Draft;
  public int Crew;
  
  public Ship(int draft, int crew)
  {
    Draft = draft;
    Crew = crew;
  }
    public bool IsWorthIt() {
      return (Draft - Crew*1.5) > 20;
    }
  
  }
__________________________________
public class Ship
{
  public int Draft;
  public int Crew;
  
  public Ship(int draft, int crew)
  {
    Draft = draft;
    Crew = crew;
  }
  
  public bool IsWorthIt() => Draft-Crew*1.5>20;
}
__________________________________
public class Ship
{
  public readonly int Draft;
  public readonly int Crew;
  
  public Ship(int draft, int crew)
  {
      Draft = draft;
      Crew = crew;
  }
  
  public object IsWorthIt() => Draft - Crew * 1.5 > 20;
}
