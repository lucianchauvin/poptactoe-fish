#include <bits/stdc++.h>
#include "bitboard.h"
#include "types.h"
using namespace Stockfish;
int main()
{
	//std::cout << SQ_B8 << '\n';
	//
	//for(const Direction& D : {NORTH,NORTH_EAST,EAST,SOUTH_EAST,SOUTH,SOUTH_WEST,WEST,NORTH_WEST})
		std::cout << shift_wrap(SOUTH,SQ_A2,2) << '\n';
	//std::cout << shift_wrap(NORTH,SQ_A1,1) << '\n';
	//std::cout << SQ_A2 << '\n';
}
