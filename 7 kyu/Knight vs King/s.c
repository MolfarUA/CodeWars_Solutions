564e1d90c41a8423230000bc


enum outcome { NONE, KING, KNIGHT };

enum outcome knight_vs_king(const int knight_pos[2], const int king_pos[2])
{
  int dx = knight_pos[0] - king_pos[0];
  int dy = knight_pos[1] - king_pos[1];
  int d = dx * dx + dy * dy;
	return d == 5 ? KNIGHT : d <= 2 ? KING : NONE;
}
_______________________________________
#include <stdlib.h>

enum outcome { NONE, KING, KNIGHT };

enum outcome knight_vs_king (const int knight_pos[2], const int king_pos[2])
{
	int y = abs(king_pos[0] - knight_pos[0]);
  int x = abs(king_pos[1] - knight_pos[1]);
  
  return x + y == 1 ? 1 : x * y > 2 ? 0 : x * y;
}
_______________________________________
#include <stdlib.h>
#include <math.h>

enum outcome { NONE, KING, KNIGHT };

enum outcome knight_vs_king (const int knight_pos[2], const int king_pos[2])
{
  if( abs(knight_pos[1] - king_pos[1]) <= 1 && abs(knight_pos[0] - king_pos[0]) <= 1 ) return KING;
  if( knight_pos[1] != king_pos[1] && knight_pos[0] != king_pos[0] && (abs(knight_pos[1] - king_pos[1]) + abs(knight_pos[0] - king_pos[0]) == 3) ) return KNIGHT;
	return NONE;
}
