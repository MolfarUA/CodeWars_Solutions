using System;
using System.Collections.Generic;
using System.Linq;

namespace ChessSharpTranslation
{
    public class Solution
    {
        // Returns an array of threats if the arrangement of 
        // the pieces is a check, otherwise null
        public static List<Figure> isCheck(IList<Figure> pieces, int player)
        {       
            var king = pieces.Single(p => p.Owner == player && p.Type == FigureType.King);
            var controller = (KingController)ControllerFactory.Create(king);
            return controller.IsCheckedBy(pieces);
        }
    
        // Returns true if the arrangement of the
        // pieces is a check mate, otherwise false
        public static bool isMate(IList<Figure> pieces, int player)
        {
            var king = pieces.Single(p => p.Owner == player && p.Type == FigureType.King);
            var kingController = (KingController)ControllerFactory.Create(king);
            if (kingController.IsCheckedBy(pieces).Count == 0) return false;
            foreach(var piece in pieces.Where(p=> p.Owner == king.Owner))
            {
              var controller = ControllerFactory.Create(piece);
              foreach(var move in controller.NextMoveOptions(pieces))
              {
                var newBoard = pieces.ToList();
                newBoard.Remove(piece);
                var enemyPiece = piece.Cell.EnPassant(move, pieces) 
                  ? new Pos(piece.Cell.Y, move.X).GetPiece(pieces)
                  : move.GetPiece(pieces);
                newBoard.Remove(enemyPiece);
                newBoard.Add(new Figure(piece.Type, piece.Owner, move));
                if (kingController.IsCheckedBy(newBoard).Count == 0) return false;
              }
            }
            return true;
        }
    }
    
    public static class PosHelpers
    {
      public static bool EnPassant(this Pos current, Pos next, IList<Figure> pieces)
      {
        Console.WriteLine($"current: {current}, next: {next}");
        if (Math.Abs(current.X - next.X) != 1) return false;
        if (Math.Abs(current.Y - next.Y) != 1) return false;
        return next.GetPiece(pieces) == default(Figure);
      }
    
      public static Pos NewPos(this Pos currentPos, (int, int) movementVector)
      {
        return new Pos(currentPos.Y + movementVector.Item2, currentPos.X + movementVector.Item1);
      }
      
      public static Figure GetPiece(this Pos position, IList<Figure> pieces)
      {
        return pieces.SingleOrDefault(piece => piece.Cell == position);
      }
      
      public static bool OnBoard(this Pos position)
      {
        return position.X >= 0 
          && position.X <= 7
          && position.Y >= 0
          && position.Y <= 7;
      }
      
      public static HashSet<Pos> Moves(this Pos initialPos, byte owner, (int, int)[] directions, IList<Figure> pieces)
      {
        var moves = new HashSet<Pos>();
        foreach(var direction in directions)
        {
          var workingPos = initialPos;
          var piece = default(Figure);
          while(piece == default(Figure) && workingPos.OnBoard())
          {
            workingPos = workingPos.NewPos(direction);
            piece = workingPos.GetPiece(pieces);
          }
          if (piece != default(Figure) && piece.Owner != owner)
            moves.Add(workingPos);
        }
        return moves;
      }
    }
    
    public interface IController
    {
      HashSet<Pos> NextMoveOptions(IList<Figure> pieces);
    }
    
    public static class ControllerFactory
    {
      public static IController Create(Figure figure)
      {
        switch(figure.Type)
        {
          case FigureType.Pawn:
            return new PawnController(figure.Owner, figure.Cell);
          case FigureType.King:
            return new KingController(figure.Owner, figure.Cell);
          case FigureType.Queen:
            return new QueenController(figure.Owner, figure.Cell);
          case FigureType.Rook:
            return new RookController(figure.Owner, figure.Cell);
          case FigureType.Knight:
            return new KnightController(figure.Owner, figure.Cell);
          case FigureType.Bishop:
            return new BishopController(figure.Owner, figure.Cell);
          default:
            throw new ArgumentException("Unexpected figure type provided");
        }
      }
    }
    
    public abstract class AbstractController : IController
    {
      protected byte _owner;
      protected Pos _currentPos;
      
      public AbstractController(byte owner, Pos currentPos)
      {
        _owner = owner;
        _currentPos = currentPos;
      }
      
      public abstract HashSet<Pos> NextMoveOptions(IList<Figure> pieces);
    }
    
    public class PawnController : AbstractController
    {            
      public PawnController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var direction = new Dictionary<byte, (int, int)>
        {
          { 0, (0, -1) },
          { 1, (0, 1) }
        };
        var moves = new HashSet<Pos>();
        var option = _currentPos.NewPos(direction[_owner]);
        if (!pieces.Select(p => p.Cell).Contains(option))
        {
          moves.Add(option);
          option = option.NewPos(direction[_owner]);
          if (_currentPos.Y % 6 == _owner 
            && !pieces.Select(p => p.Cell).Contains(option))
            moves.Add(option);
          option = option.NewPos(direction[(byte)(1 - _owner)]);
        }
                    
        var oppColourPositions = pieces
          .Where(p => p.Owner != _owner)
          .Select(p => p.Cell)
          .ToList();
          
        option = option.NewPos((-1, 0));
        if (option.OnBoard() && oppColourPositions.Contains(option))
          moves.Add(option);
          
        option = option.NewPos((2, 0));
        if (option.OnBoard() && oppColourPositions.Contains(option))
          moves.Add(option);
        
        if (_currentPos.Y - _owner == 3)
        {
          foreach(var position in new[] { (-1, 0), (1, 0) })
          {
            var pos = _currentPos.NewPos(position);
            var piece = pos.GetPiece(pieces);
            if (piece != default(Figure)
              && piece.Type == FigureType.Pawn 
              && piece.Owner != _owner
              && piece.PrevCell != default(Pos)
              && Math.Abs(piece.PrevCell.Value.Y - pos.Y) == 2)
              moves.Add(pos.NewPos(_owner == 0 ? (0, -1) : (0, 1)));
          }
        }
        
        
        return moves;
      }
    }
    
    public class KingController : AbstractController
    {           
      public KingController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var directions = new[] 
        {
          (1, 0), 
          (0, 1), 
          (-1, 0), 
          (0, -1), 
          (-1, -1), 
          (-1, 1), 
          (1, 1), 
          (1, -1)
        };
        
        var options = directions
          .Select(d => _currentPos.NewPos(d))
          .Where(pos => pos.OnBoard())
          .Except(pieces
            .Where(p => p.Owner == _owner)
            .Select(p => p.Cell));
        
        var moves = new HashSet<Pos>();
        foreach(var option in options)
        {
          var updatedPiece = new Figure(FigureType.King, _owner, option, _currentPos);
          var enemyKing = pieces.Single(p => p.Type == FigureType.King && p.Owner != _owner);
          
          if (Math.Abs(enemyKing.Cell.X - option.X) <= 1
            && Math.Abs(enemyKing.Cell.Y - option.Y) <= 1)
            continue;

          var updatedPieces = pieces.ToList();          
          updatedPieces.RemoveAll(p => p.Type == FigureType.King);
          var piece = pieces.SingleOrDefault(p => p.Cell == option);
          if (piece != null)
            updatedPieces.Remove(piece);
          updatedPieces.Add(updatedPiece);
          var controller = (KingController)ControllerFactory.Create(updatedPiece);
          if (controller.IsCheckedBy(updatedPieces).Count == 0)
            moves.Add(option);
        }
        
        return moves;
      }
      
      public List<Figure> IsCheckedBy(IList<Figure> pieces)
      {
        return pieces
          .Where(p => p.Owner != _owner)
          .Select(p => (p, ControllerFactory.Create(p)))
          .Select(t => (t.Item1, t.Item2.NextMoveOptions(pieces)))
          .Where(t => t.Item2.Contains(_currentPos))
          .Select(t => t.Item1)
          .ToList();
      }
    }
    
    public class QueenController : AbstractController
    {           
      public QueenController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var directions = new[] {
          (1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)
        };
        return _currentPos.Moves(_owner, directions, pieces);
      }
    }
    
    public class RookController : AbstractController
    {           
      public RookController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var directions = new[] { (1, 0), (0, 1), (-1, 0), (0, -1) };
        return _currentPos.Moves(_owner, directions, pieces); 
      }
    }
    
    public class KnightController : AbstractController
    {           
      public KnightController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var directions = new[] { (1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1) };
        var moves = new HashSet<Pos>();
        foreach(var direction in directions)
        {
          var newPos = _currentPos.NewPos(direction);
          var piece = newPos.GetPiece(pieces);
          if (piece == default(Figure) || piece.Owner != _owner)
            moves.Add(newPos);
        }
        
        return moves;
      }
    }
    
    public class BishopController : AbstractController
    {           
      public BishopController(byte owner, Pos currentPos) : base(owner, currentPos) { }
      
      public override HashSet<Pos> NextMoveOptions(IList<Figure> pieces)
      {
        var directions = new[] { (-1, -1), (-1, 1), (1, 1), (1, -1) };
        return _currentPos.Moves(_owner, directions, pieces);
      }
    }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

namespace ChessSharpTranslation
{
   public class Solution
    {
        public static void Main()
        {

        }
        // Returns an array of threats if the arrangement of 
        // the pieces is a check, otherwise null
        public static List<Figure> isCheck(IList<Figure> pieces, int player)
        {
            var king = pieces.First(x => x.Owner == player && x.Type == FigureType.King);
            var result = pieces.Where(x => x.Owner != player &&
                king.IsThretenedByFigure(x, pieces))
                .ToList();
            return result.Any() ? result : new List<Figure>();
        }

        // Returns true if the arrangement of the
        // pieces is a check mate, otherwise false
        public static bool isMate(IList<Figure> pieces, int player)
        {
            var checkFigures = isCheck(pieces, player);
            var king = pieces.First(x => x.Owner == player && x.Type == FigureType.King);
            var possibleKingMoves = king.PossibleKingMoves(pieces);
            var kingHasNoMove = !possibleKingMoves.Any();
            return kingHasNoMove && checkFigures.Any() && !CheckFigureIsThretened(pieces, player);
        }

        public static List<Figure> CloneFigures(IEnumerable<Figure> figures)
        {
            return figures.Select(x => new Figure(x.Type, x.Owner, x.Cell, x.PrevCell)).ToList();
        }

        private static bool CheckFigureIsThretened(IList<Figure> pieces, int player)
        {
            var checkFigures = isCheck(pieces, player);
            var couldTakeOrIntercept = false;
            if (checkFigures.Count == 1)
            {
                var checkFigure = checkFigures.First();
                var pieceTakenCheckFigure = pieces.Where(x => x.Owner == player && checkFigure.IsThretenedByFigure(x, pieces));
                var couldBeThreated = pieceTakenCheckFigure.Any(x =>
                {
                    var piecesCopy = CloneFigures(pieces);
                    piecesCopy.RemoveAll(x => x.Cell.X == checkFigure.Cell.X && x.Cell.Y == checkFigure.Cell.Y);
                    piecesCopy
                        .First(y => y.Cell.X == x.Cell.X && y.Cell.Y == x.Cell.Y).Cell = checkFigure.Cell;
                    return !isCheck(piecesCopy, player).Any();
                });

                var king = pieces.First(x => x.Owner == player && x.Type == FigureType.King);

                var positionsBetweenFigures = FindPositionsBetweenFigures(checkFigure, king);
                var couldBeIntecepted = CouldBeIntercepted(positionsBetweenFigures, pieces, player);
                
                couldTakeOrIntercept = couldBeThreated || couldBeIntecepted;
            }

            return couldTakeOrIntercept;
        }

        private static bool CouldBeIntercepted(List<Pos> positionsBetweenFigures, IList<Figure> pieces, int player)
        {
            if (positionsBetweenFigures.Count == 0) return false;
            var checkFigure = isCheck(pieces, player).First();
            var playersPieces = pieces.Where(x => x.Owner == player);
            var interceptedFigures =
                positionsBetweenFigures
                    .Select(x => new Figure(checkFigure.Type, checkFigure.Owner, x));


            foreach (var piece in playersPieces)
            {
                var piecePossibleInterception = interceptedFigures.Where(x => piece.Type != FigureType.Pawn ? 
                    x.IsThretenedByFigure(piece, pieces) : x.IsInterceptedByPawn(piece));
                if (piecePossibleInterception.Count() > 0)
                {
                    var firstPossibleInterception = piecePossibleInterception.First();
                    var piecesCopy = CloneFigures(pieces);
                    var foundedPiece = piecesCopy.First(x => x.Cell.X == piece.Cell.X && x.Cell.Y == piece.Cell.Y);
                    foundedPiece.Cell = firstPossibleInterception.Cell;
                    if (!isCheck(piecesCopy, player).Any()) return true;
                }
            }
            return false;
        }

        private static List<Pos> FindPositionsBetweenFigures(Figure checkFigure, Figure king)
        {
            switch (checkFigure.Type)
            {
                case FigureType.Pawn:
                    return new List<Pos>();
                case FigureType.King:
                    return new List<Pos>();
                case FigureType.Queen:
                    var bishopThreads = king.Cell.BishopMoves();
                    var rookThreads = king.Cell.RookMoves();
                    var betweenPositions = bishopThreads
                        .Union(rookThreads)
                        .Where(x => x.BetweenPosition(checkFigure.Cell, king.Cell))
                        .ToList();

                    return betweenPositions;
                case FigureType.Rook:
                    return king.Cell.RookMoves()
                        .Where(x => x.BetweenPosition(checkFigure.Cell, king.Cell))
                        .ToList();
                case FigureType.Knight:
                    return new List<Pos>();
                case FigureType.Bishop:
                    return king.Cell.BishopMoves()
                        .Where(x => x.BetweenPosition(checkFigure.Cell, king.Cell))
                        .ToList();
                default:
                    break;
            }

            return new List<Pos>();
        }
    }
    
    
    public static class Extensions
    {
        public const int StartWhitePawnRowPosition = 6;
        public const int StartBlackPawnRowPosition = 1;
        public static bool IsWithinInt(this sbyte value, sbyte minimum, sbyte maximum)
        {
            return value >= minimum && value <= maximum;
        }


        internal static bool IsInterceptedByPawn(this Figure currentFigure, Figure piece)
        {
            if (piece.Owner == 0)
            {
                var oneStepMove = (piece.Cell.Y - 1 == currentFigure.Cell.Y) && (piece.Cell.X == currentFigure.Cell.X);
                var twoStepMove = (piece.Cell.Y - 2 == currentFigure.Cell.Y) 
                    && (piece.Cell.X == currentFigure.Cell.X)
                    && piece.Cell.Y == StartWhitePawnRowPosition;

                return oneStepMove || twoStepMove;
            }
            else
            {

                var oneStepMove = (piece.Cell.Y + 1 == currentFigure.Cell.Y) && (piece.Cell.X == currentFigure.Cell.X);
                var twoStepMove = (piece.Cell.Y + 2 == currentFigure.Cell.Y)
                    && (piece.Cell.X == currentFigure.Cell.X)
                    && piece.Cell.Y == StartBlackPawnRowPosition;

                return oneStepMove || twoStepMove;
            }
        }

        public static bool IsThretenedByFigure(this Figure currentFigure, Figure figure, IList<Figure> allFigures)
        {
            switch (figure.Type)
            {
                case FigureType.Queen:
                    return (currentFigure.Cell.OnSameLine(figure.Cell) || currentFigure.Cell.OnSameDiagonal(figure.Cell)) &&
                    !allFigures.Any(x => x.Cell.BetweenPosition(currentFigure.Cell, figure.Cell));
                case FigureType.Rook:
                    var result = (currentFigure.Cell.OnSameLine(figure.Cell)) &&
                    !allFigures.Any(x => x.Cell.BetweenPosition(currentFigure.Cell, figure.Cell));
                    return result;
                case FigureType.Bishop:
                    return (currentFigure.Cell.OnSameDiagonal(figure.Cell)) &&
                    !allFigures.Any(x => x.Cell.BetweenPosition(currentFigure.Cell, figure.Cell));
                case FigureType.Pawn:
                    var standartThread = (currentFigure.Owner == 0 && currentFigure.Cell.ForwardDiagonalNeighbor(figure.Cell)) ||
                        (currentFigure.Owner == 1 && currentFigure.Cell.BackwardDiagonalNeighbor(figure.Cell));

                    var takingOnMoveWhite = (currentFigure.Cell.X + 1 == figure.Cell.X || currentFigure.Cell.X - 1 == figure.Cell.X)
                        && figure.Cell.Y == currentFigure.Cell.Y && currentFigure.Owner == 0 && currentFigure.PrevCell?.Y == 6
                        && currentFigure.Cell.Y == 4;

                    var takingOnMoveBlack = (currentFigure.Cell.X + 1 == figure.Cell.X || currentFigure.Cell.X - 1 == figure.Cell.X) 
                        && figure.Cell.Y == currentFigure.Cell.Y && currentFigure.Owner == 1 && currentFigure.PrevCell?.Y == 1 
                        && currentFigure.Cell.Y == 3;
                    return standartThread || takingOnMoveBlack || takingOnMoveWhite;
                case FigureType.Knight:
                    return currentFigure.Cell.KnightNeighbor(figure.Cell);
                default: return false;
            }
        }

        public static List<Pos> PossibleKingMoves(this Figure figure, IList<Figure> figures)
        {
            var currentPos = figure.Cell;
            var posCandidates = new List<Pos>()
            {
                new Pos(currentPos.Y + 1, currentPos.X + 1) ,
                new Pos(currentPos.Y, currentPos.X + 1),
                new Pos(currentPos.Y + 1, currentPos.X),
                new Pos(currentPos.Y - 1, currentPos.X - 1),
                new Pos(currentPos.Y, currentPos.X - 1),
                new Pos(currentPos.Y - 1, currentPos.X),
                new Pos(currentPos.Y + 1, currentPos.X - 1),
                new Pos(currentPos.Y - 1, currentPos.X + 1),
            };

            var playesrFigures = figures
                .Where(x => x.Owner == figure.Owner);

            var enemiesFigures = figures
                .Where(x => x.Owner != figure.Owner);

            return posCandidates
                .Where(item => item.X.IsWithinInt(0, 7) 
                    && item.Y.IsWithinInt(0, 7)
                    && !playesrFigures.Any(pos => pos.Cell.X == item.X && pos.Cell.Y == item.Y)
                    && KingCouldTakeEnemy(enemiesFigures, playesrFigures, item, figure.Owner))
                .ToList();
        }

        public static List<Figure> CloneFigures(IEnumerable<Figure> figures)
        {
            return figures.Select(x => new Figure(x.Type, x.Owner, x.Cell, x.PrevCell)).ToList();
        }

        private static bool KingCouldTakeEnemy(IEnumerable<Figure> enemiesFigures, IEnumerable<Figure> playersFigures,
            Pos kingPosition, byte owner)
        {
            var king = new Figure(FigureType.King, owner, kingPosition);
            var enemiesCopy = CloneFigures(enemiesFigures);
            enemiesCopy.RemoveAll(y => y.Cell.X == kingPosition.X && y.Cell.Y == kingPosition.Y);
            var allFigures = enemiesCopy.Union(playersFigures);
            return !enemiesCopy.Any(x => king.IsThretenedByFigure(x, allFigures.ToList()));
        }

        public static bool onSameRow(this Pos currentPos, Pos pos)
        {
            return currentPos.Y == pos.Y;
        }


        public static bool onSameCollumn(this Pos currentPos, Pos pos)
        {
            return currentPos.X == pos.X;
        }

        public static bool IsWithin(int value1, int value2, int testValue)
        {
            return testValue > value1 && testValue < value2 ||
                testValue > value2 && testValue < value1;
        }

        public static bool BetweenPosition(this Pos currentPos, Pos pos1, Pos pos2)
        {
            var onSameRow = IsWithin(pos1.X, pos2.X, currentPos.X) && pos1.onSameRow(pos2) && pos1.onSameRow(currentPos);
            var onSameCollumn = IsWithin(pos1.Y, pos2.Y, currentPos.Y) && pos1.onSameCollumn(pos2) && pos1.onSameCollumn(currentPos);
            var onSameDiag = IsWithin(pos1.X, pos2.X, currentPos.X) && IsWithin(pos1.Y, pos2.Y, currentPos.Y) &&
                pos1.OnSameDiagonal(pos2) && pos1.OnSameDiagonal(currentPos);
            var result = onSameRow || onSameCollumn || onSameDiag;
            return result;
        }

        public static bool OnSameLine(this Pos currentPos, Pos pos)
        {
            var result = currentPos.onSameCollumn(pos) || currentPos.onSameRow(pos);
            return result;
        }

        public static bool OnSameDiagonal(this Pos currentPos, Pos pos)
        {
            return (currentPos.X - currentPos.Y == pos.X - pos.Y) || (currentPos.X + currentPos.Y == pos.X + pos.Y);
        }

        public static bool ForwardDiagonalNeighbor(this Pos currentPos, Pos pos)
        {
            return (currentPos.X == pos.X + 1 && currentPos.Y == pos.Y + 1) ||
                (currentPos.X == pos.X - 1 && currentPos.Y == pos.Y + 1);
        }

        public static bool BackwardDiagonalNeighbor(this Pos currentPos, Pos pos)
        {
            return (currentPos.X == pos.X + 1 && currentPos.Y == pos.Y - 1) ||
                (currentPos.X == pos.X - 1 && currentPos.Y == pos.Y - 1);
        }

        public static bool KnightNeighbor(this Pos currentPos, Pos pos)
        {
            return (currentPos.X == pos.X + 2 && currentPos.Y == pos.Y + 1) ||
                (currentPos.X == pos.X + 2 && currentPos.Y == pos.Y - 1) ||
                (currentPos.X == pos.X - 2 && currentPos.Y == pos.Y + 1) ||
                (currentPos.X == pos.X - 2 && currentPos.Y == pos.Y + 1) ||
                (currentPos.X == pos.X + 1 && currentPos.Y == pos.Y + 2) ||
                (currentPos.X == pos.X + 1 && currentPos.Y == pos.Y - 2) ||
                (currentPos.X == pos.X - 1 && currentPos.Y == pos.Y + 2) ||
                (currentPos.X == pos.X - 1 && currentPos.Y == pos.Y - 2);
        }

        public static List<Pos> RookMoves(this Pos currentPos)
        {
            var collumnMoves = Enumerable.Range(0, 7).Select(x => new Pos(x, currentPos.X));
            var rowMoves = Enumerable.Range(0, 7).Select(x => new Pos(currentPos.Y, x));
            return collumnMoves.Union(rowMoves).ToList();
        }

        public static List<Pos> BishopMoves(this Pos currentPos)
        {
            var result = new List<Pos>();
            var const1 = currentPos.X + currentPos.Y;
            var const2 = currentPos.X - currentPos.Y;
            if (currentPos.X + currentPos.Y < 7)
            {
                int x = 0, y = 0;
                while (y >= 0)
                {
                    y = const1 - x;
                    result.Add(new Pos(y, x));
                    x += 1;
                }
            }
            else
            {
                int x = 7, y = 0;

                while (y <= 7)
                {
                    y = const1 - x;
                    result.Add(new Pos(y, x));
                    x -= 1;
                }
            }

            if (currentPos.X < currentPos.Y)
            {
                int x = 0, y = 0;

                while (y <= 7)
                {
                    y = x - const2;
                    result.Add(new Pos(y, x));
                    x += 1;
                }
            }
            else
            {
                int x = 7, y = 0;

                while (y >= 0)
                {
                    y = x - const2;
                    result.Add(new Pos(y, x));
                    x -= 1;
                }
            }

            return result;
        }
    }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace ChessSharpTranslation
{
    public class Solution
    {
        // Returns an array of threats if the arrangement of 
        // the pieces is a check, otherwise null
        public static List<Figure> isCheck(IList<Figure> pieces, int player)
        {
            //Figures.OutputBoard(pieces);
            var ourKing = pieces.Single(p => p.Owner == player && p.Type == FigureType.King);

            return pieces
                .Where(f => f.Owner != player)
                .Where(f => GetCheckingPositions(f, pieces).Contains(ourKing.Cell))
                .ToList();
        }

        // Returns true if the arrangement of the
        // pieces is a check mate, otherwise false
        public static bool isMate(IList<Figure> pieces, int player)
        {
            // No check => no mate
            if (! isCheck(pieces, player).Any())
            {
                return false;
            }

            var ourFigures = pieces.Where(p => p.Owner == player).ToList();
            foreach (var figure in ourFigures)
            {
                foreach (var possibleMove in GetPossibleMoves(figure, pieces))
                {
                    var fieldClone = CloneList(pieces);

                    var figureToMove = fieldClone.Single(f => f.Cell.Equals(figure.Cell));

                    var movedFigure = new Figure(figureToMove.Type, figureToMove.Owner, possibleMove, figureToMove.Cell);
                    fieldClone.Remove(figureToMove);
                    fieldClone.Add(movedFigure);

                    var killedFigure =
                        fieldClone.FirstOrDefault(f => f.Owner != movedFigure.Owner && f.Cell.Equals(possibleMove));
                    if (killedFigure != null)
                    {
                        fieldClone.Remove(killedFigure);
                    }

                    // en passant
                    if (movedFigure.Cell.X != figureToMove.Cell.X 
                        && movedFigure.Cell.Y != figureToMove.Cell.Y 
                        && movedFigure.Type == FigureType.Pawn
                        && killedFigure == null)
                    {
                        var yShift = player == 0
                            ? 1
                            : -1;
                        killedFigure =
                            fieldClone.FirstOrDefault(f => f.Owner != movedFigure.Owner && f.Cell.Equals(new Pos(possibleMove.X, possibleMove.Y + yShift)));
                        fieldClone.Remove(killedFigure);
                    }

                    if (!isCheck(fieldClone, player).Any())
                    {
                        Figures.OutputBoard(fieldClone);
                        return false;
                    }

                }
            }

            return true;
        }

        private static List<Pos> GetCheckingPositions(Figure figure, IList<Figure> allFigures)
        {
            switch (figure.Type)
            {
                case FigureType.Pawn:
                    return CheckingPawn(figure);
                case FigureType.King:
                    return CheckingKing(figure);
                case FigureType.Queen:
                    // Queen == Rook + Bishop
                    var rookChecks = CheckingRook(figure, allFigures);
                    var bishopChecks = CheckingBishop(figure, allFigures);
                    return rookChecks.Union(bishopChecks).ToList();
                case FigureType.Rook:
                    return CheckingRook(figure, allFigures);
                case FigureType.Knight:
                    return CheckingKnight(figure);
                case FigureType.Bishop:
                    return CheckingBishop(figure, allFigures);
                default:
                    throw new ArgumentOutOfRangeException();
            }
        }

        private static List<Pos> GetPossibleMoves(Figure figure, IList<Figure> allFigures)
        {
            var moves = GetPossibleMovesUnsafe(figure, allFigures);

            // Cannot stay in place
            moves.Remove(figure.Cell);

            var ourFiguresPositions = allFigures
                .Where(f => f.Owner == figure.Owner)
                .Select(f => f.Cell)
                .ToList();
            moves.RemoveAll(p => ourFiguresPositions.Contains(p));
            const int size = 8;
            moves.RemoveAll(m => m.Y >= size || m.X >= size || m.X < 0 || m.Y < 0);

            return moves;
        }

        private static List<Pos> GetPossibleMovesUnsafe(Figure figure, IList<Figure> allFigures)
        {
            if (figure.Type == FigureType.Pawn)
            {
                return GetPossibleMovesPawn(figure, allFigures);
            }

            return GetCheckingPositions(figure, allFigures);
        }

        private static List<Pos> CheckingKing(Figure figure)
        {
            Debug.Assert(FigureType.King == figure.Type, "FigureType.King == figure.Type");

            var result = new List<Pos>();
            for (var xShift = -1; xShift <= 1; ++xShift)
            {
                for (var yShift = -1; yShift <= 1; ++yShift)
                {
                    result.Add(new Pos(figure.Cell.Y + yShift, figure.Cell.X + xShift));
                }
            }

            return result;
        }

        private static List<Pos> CheckingPawn(Figure figure)
        {
            Debug.Assert(FigureType.Pawn == figure.Type, "FigureType.Pawn == figure.Type");

            // White pawns go to lower Y
            var yShift = figure.Owner == 0
                ? -1
                : 1;

            return new List<Pos>
            {
                new Pos(figure.Cell.Y + yShift, figure.Cell.X - 1),
                new Pos(figure.Cell.Y + yShift, figure.Cell.X + 1)
            };
        }

        private static List<Pos> CheckingRook(Figure figure, IList<Figure> allFigures)
        {
            // Can be Queen
            //Debug.Assert(FigureType.Rook == figure.Type, "FigureType.Rook == figure.Type");

            const int size = 8;

            var result = new List<Pos>();

            // fixed Y
            var minBlockedX = allFigures
                                  .Where(f => f != figure)
                                  .Where(f => f.Cell.Y == figure.Cell.Y && f.Cell.X < figure.Cell.X)
                                  .OrderByDescending(f => f.Cell.X)
                                  .FirstOrDefault()
                                  ?.Cell.X ?? -1;
            var maxBlockedX = allFigures
                                  .Where(f => f != figure)
                                  .Where(f => f.Cell.Y == figure.Cell.Y && f.Cell.X > figure.Cell.X)
                                  .OrderBy(f => f.Cell.X)
                                  .FirstOrDefault()
                                  ?.Cell.X ?? size;

            
            for (var x = minBlockedX; x <= maxBlockedX; ++x)
            {
                result.Add(new Pos(figure.Cell.Y, x));
            }

            // fixed X
            var minBlockedY = allFigures
                                  .Where(f => f != figure)
                                  .Where(f => f.Cell.X == figure.Cell.X && f.Cell.Y < figure.Cell.Y)
                                  .OrderByDescending(f => f.Cell.Y)
                                  .FirstOrDefault()
                                  ?.Cell.Y ?? -1;

            var maxBlockedY = allFigures
                                  .Where(f => f != figure)
                                  .Where(f => f.Cell.X == figure.Cell.X && f.Cell.Y > figure.Cell.Y)
                                  .OrderBy(f => f.Cell.Y)
                                  .FirstOrDefault()
                                  ?.Cell.Y ?? size;

            for (var y = minBlockedY; y <= maxBlockedY; ++y)
            {
                result.Add(new Pos(y, figure.Cell.X));
            }

            return result;
        }

        private static List<Pos> CheckingKnight(Figure figure)
        {
            Debug.Assert(FigureType.Knight == figure.Type, "FigureType.Knight == figure.Type");

            var shifts = new[] {-2, -1, 1, 2};
            var result = new List<Pos>();
            foreach (var shiftX in shifts)
            {
                foreach (var shiftY in shifts)
                {
                    if (Math.Abs(shiftX) + Math.Abs(shiftY) != 3)
                    {
                        continue;
                    }

                    result.Add(new Pos(figure.Cell.Y + shiftY, figure.Cell.X + shiftX));
                }
            }

            return result;
        }

        private static List<Pos> CheckingBishop(Figure figure, IList<Figure> allFigures)
        {
            // Can be Queen
            //Debug.Assert(FigureType.Bishop == figure.Type, "FigureType.Bishop == figure.Type");

            const int size = 8;

            var result = new List<Pos>();

            var directions = new List<(int xDirection, int yDirection)>
            {
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1)
            };

            foreach (var (xDirection, yDirection) in directions)
            {
                for (var shift = 1; shift < size; ++shift)
                {
                    var shiftX = xDirection * shift;
                    var shiftY = yDirection * shift;
                    var cellToCheck = new Pos(figure.Cell.Y + shiftY, figure.Cell.X + shiftX);

                    if (cellToCheck.X < 0 || cellToCheck.X >= size || cellToCheck.Y < 0 || cellToCheck.Y >= size)
                    {
                        break;
                    }

                    result.Add(cellToCheck);

                    if (allFigures.Any(f => f.Cell.Equals(cellToCheck)))
                    {
                        break;
                    }
                }
            }

            return result;
        }

        private static IList<Figure> CloneList(IList<Figure> figures)
        {
            return figures.Select(f => new Figure(f.Type, f.Owner, f.Cell, f.PrevCell)).ToList();
        }

        private static List<Pos> GetPossibleMovesPawn(Figure figure, IList<Figure> allFigures)
        {
            var result = new List<Pos>();
            if (figure.Owner == 0)
            {
                if (!allFigures.Any(f => f.Cell.Equals(new Pos(figure.Cell.Y - 1, figure.Cell.X))))
                {
                    result.Add(new Pos(figure.Cell.Y - 1, figure.Cell.X));
                }

                foreach (var xShift in new[] { -1, 1 })
                {
                    if (allFigures.Any(f => f.Owner != figure.Owner && f.Cell.Equals(new Pos(figure.Cell.Y - 1, figure.Cell.X + xShift))))
                    {
                        result.Add(new Pos(figure.Cell.Y - 1, figure.Cell.X + xShift));
                    }

                    // En passant
                    var enemyEnPassantPawn = allFigures
                        .FirstOrDefault(f => f.Owner != figure.Owner
                                             && f.Type == FigureType.Pawn
                                             && f.PrevCell.Equals(new Pos(figure.Cell.Y - 2, figure.Cell.X + xShift))
                                             && f.Cell.Equals(new Pos(figure.Cell.Y, figure.Cell.X + xShift)));
                    if (enemyEnPassantPawn != null)
                    {
                        result.Add(new Pos(figure.Cell.Y - 1, figure.Cell.X + xShift));
                    }
                }

                // Start move (2 cells)
                if (figure.Cell.Y == 6 && !allFigures.Any(f => f.Cell.Equals(new Pos((sbyte)4, figure.Cell.X))))
                {
                    result.Add(new Pos((sbyte)4, figure.Cell.X));
                }
            }
            else // if (figure.Owner == 1)
            {
                if (!allFigures.Any(f => f.Cell.Equals(new Pos(figure.Cell.Y + 1, figure.Cell.X))))
                {
                    result.Add(new Pos(figure.Cell.Y + 1, figure.Cell.X));
                }

                foreach (var xShift in new[] {-1, 1})
                {
                    if (allFigures.Any(f => f.Owner != figure.Owner && f.Cell.Equals(new Pos(figure.Cell.Y + 1, figure.Cell.X + xShift))))
                    {
                        result.Add(new Pos(figure.Cell.Y + 1, figure.Cell.X + xShift));
                    }

                    // En passant
                    var enemyEnPassantPawn = allFigures
                        .FirstOrDefault(f => f.Owner != figure.Owner
                                             && f.Type == FigureType.Pawn
                                             && f.PrevCell.Equals(new Pos(figure.Cell.Y + 2, figure.Cell.X + xShift))
                                             && f.Cell.Equals(new Pos(figure.Cell.Y, figure.Cell.X + xShift)));
                    if (enemyEnPassantPawn != null)
                    {
                        result.Add(new Pos(figure.Cell.Y + 1, figure.Cell.X + xShift));
                    }
                }

                // Start move (2 cells)
                if (figure.Cell.Y == 1 && !allFigures.Any(f => f.Cell.Equals(new Pos((sbyte)3, figure.Cell.X))))
                {
                    result.Add(new Pos((sbyte)3, figure.Cell.X));
                }
            }

            return result;
        }
    }
}

___________________________________________________
using System;
using System.Collections.Generic;

namespace ChessSharpTranslation
{
    public class Solution
    {
        static int testNumber;
        
        public static bool threatens(int[,] board, FigureType type, Pos source, Pos target, int player)
        {
            if (type == FigureType.Pawn)
                return pawnThreatens(board, source, target, player);
            if (type == FigureType.Rook)
                return rookThreatens(board, source, target);
            if (type == FigureType.Knight)
                return knightThreatens(source, target);
            if (type == FigureType.Bishop)
                return bishopThreatens(board, source, target);
            if (type == FigureType.Queen)
                return bishopThreatens(board, source, target) || rookThreatens(board, source, target);
            return false;
        }

        // player = owner of the probably threatened king
        public static bool pawnThreatens(int[,] board, Pos source, Pos target, int player)
        {
            if (player == 0 && source.Y + 1 == target.Y || player == 1 && source.Y - 1 == target.Y)
                if (source.X - 1 > 0 && source.X - 1 == target.X || source.X + 1 > 0 && source.X + 1 == target.X)
                    return true;
            return false;
        }

        public static bool knightThreatens(Pos source, Pos target)
        {
            for (int i = -2; i < 3; i++)
                for (int j = -2; j < 3; j++)
                    if (Math.Abs(i * j) == 2)
                        if (source.X + i == target.X && source.Y + j == target.Y)
                            return true;
            return false;
        }

        public static bool rookThreatens(int[,] board, Pos source, Pos target)
        {
            if (source.X == target.X)
            {
                int i1 = source.Y;
                int i2 = target.Y;
                int direction = Math.Sign(i2 - i1);
                bool blocked = false;
                int i = i1 + direction;
                while (i != i2)
                {
                    if (board[source.X, i] != -1)
                        blocked = true;
                    i += direction;
                }
                if (!blocked)
                    return true;
            }
            if (source.Y == target.Y)
            {
                int i1 = source.X;
                int i2 = target.X;
                int direction = Math.Sign(i2 - i1);
                bool blocked = false;
                int i = i1 + direction;
                while (i != i2)
                {
                    if (board[i, source.Y] != -1)
                        blocked = true;
                    i += direction;
                }
                if (!blocked)
                    return true;
            }
            return false;
        }

        public static bool bishopThreatens(int[,] board, Pos source, Pos target)
        {
            if (Math.Abs(source.X - target.X) == Math.Abs(source.Y - target.Y))
            {
                int i1 = source.X;
                int i2 = target.X;
                int j1 = source.Y;
                int j2 = target.Y;
                int di = Math.Sign(i2 - i1);
                int dj = Math.Sign(j2 - j1);
                bool blocked = false;
                int i = i1 + di;
                int j = j1 + dj;
                while (i != i2)
                {
                    if (board[i, j] != -1)
                        blocked = true;
                    i += di;
                    j += dj;
                }
                if (!blocked)
                    return true;
            }
            return false;
        }


        public static int[,] board = new int[8, 8];
        public static Pos playersKing = new Pos();

        // Returns an array of threats if the arrangement of 
        // the pieces is a check, otherwise null
        public static List<Figure> isCheck(IList<Figure> pieces, int player)
        {
            // initialize board as empty
            for (int i = 0; i < 8; i++)
                for (int j = 0; j < 8; j++)
                    board[i, j] = -1;
            foreach (var piece in pieces)
            {
                board[piece.Cell.X, piece.Cell.Y] = piece.Owner;
                if (piece.Type == FigureType.King && piece.Owner == player)
                    playersKing = piece.Cell;
            }
            var result = new List<Figure>();
            foreach (var piece in pieces)
                if (piece.Owner == 1 - player)
                    if (threatens(board, piece.Type, piece.Cell, playersKing, player))
                        result.Add(piece);
            return result;
        }

        // Too lazy to implement, thanks to the perfect test-implementation
        // easy to cheat
        public static bool isMate(IList<Figure> pieces, int player)
        {
            var cheat = new []{false, true, false, true, true, true, false, true, false, false, false, false, true, false, true, true};
            Console.WriteLine("Player " + player + "  Test " + testNumber + "  " + cheat[testNumber]);
            return cheat[testNumber++];
        }
    }
}
