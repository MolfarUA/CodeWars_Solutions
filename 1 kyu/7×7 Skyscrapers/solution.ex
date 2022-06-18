5917a2205ffc30ec3a0000a8

defmodule PuzzleSolver do

  @size 7
  
  def visibility(x), do: visibility(x, 0)
  def visibility([], _), do: 0
  def visibility([x], prev_max) when prev_max < x, do: 1
  def visibility([@size | _xs], _prev_max), do: 1
  def visibility([x | xs], prev_max) when prev_max < x, do: 1 + visibility(xs, x) 
  def visibility([x | xs], prev_max) when prev_max > x, do: visibility(xs, prev_max) 
  
  def permutations([]), do:  [[]]
  def permutations(list) do
    for h <- list, t <- permutations(Enum.to_list(list) -- [h]), do: [h | t]
  end
  
  def visibility_for_hint(0), do: 1..@size |> permutations
  def visibility_for_hint(hint) do
    1..@size
    |> permutations()
    |> Enum.group_by(&visibility/1)
    |> Map.get(hint)
  end
  
  def visibility_for_hints(hint1, hint2) do
    v1 = visibility_for_hint(hint1) |> MapSet.new()
    v2 = visibility_for_hint(hint2) |> Enum.map(&Enum.reverse/1) |> MapSet.new()
    MapSet.intersection(v1, v2)
  end
    
  def filter_vset([], _, _), do: MapSet.new()
  def filter_vset(_, _, []), do: MapSet.new()
  def filter_vset(vset, i, values) do
    vset
    |> Enum.filter(fn p -> Enum.member?(values, Enum.at(p, i)) end)
    |> MapSet.new()
  end
  
  def cross_vsets(vset1, i1, vset2, i2) do
    vset1 = filter_vset(vset1, i1, Enum.map(vset2, &(Enum.at(&1, i2))) |> Enum.uniq)
    vset2 = filter_vset(vset2, i2, Enum.map(vset1, &(Enum.at(&1, i1))) |> Enum.uniq)
    {vset1, vset2}
  end
  
  def counts(sets) do
    sets
    |> Enum.map(&Enum.count/1)
  end
  
  def count(sets) do
    sets
    |> counts()
    |> Enum.reduce(&+/2)
  end
    
  def run_crosses({horizontals, verticals}) do
    
    hvcounts = {count(horizontals), count(verticals)}
    
    if elem(hvcounts,0) <= @size do
      { horizontals, verticals }
    else
      horizontals 
      |> Enum.with_index()
      |> Enum.map_reduce(verticals, fn {hset, i}, verticals -> 

        {verticals, hset} = verticals 
        |> Enum.with_index()
        |> Enum.map_reduce(hset, fn {vset, j}, hset ->

          cross_vsets(vset, i, hset, j)
        end)

        {hset, verticals}
      end)
      |> break_ties(hvcounts)
    end
  end
  
  def break_ties({horizontals, verticals} = both, hvcounts) do
    if {count(horizontals), count(verticals)} == hvcounts do
      sorted_with_index = horizontals
      |> Enum.with_index()
      |> Enum.sort_by(fn {h, _i} -> Enum.count(h) end)
      
      Enum.find_value(sorted_with_index, fn {h, i} ->
        Enum.find_value(h, fn set -> 
          horizontals = List.replace_at(horizontals, i, MapSet.new([set]))
          {horizontals, verticals} = run_crosses({horizontals, verticals})

          if Enum.member?(counts(horizontals), 0) || Enum.member?(counts(verticals), 0) do
            nil
          else
            {horizontals, verticals}
          end
        end)
      end)
    else
      run_crosses(both)
    end
  end
    
    
    
  def solve(clues) do
  
    {horizontals, _verticals} =
      {Enum.map(@size..(@size*2 - 1), fn n -> visibility_for_hints(Enum.at(clues, (@size*5-1)-n), Enum.at(clues, n)) end),
       Enum.map(0..(@size - 1), fn n -> visibility_for_hints(Enum.at(clues, n), Enum.at(clues, (@size*3-1)-n)) end)}
      |>  run_crosses()
    
    horizontals
    |> Enum.map(&MapSet.to_list/1)
    |> Enum.map(&List.flatten/1)
    
  end
end
______________________________________________
defmodule PuzzleSolver do
  @all [0,1,2,3,4,5,6]
  @floors [1,2,3,4,5,6,7]

  def solve(clues) do
    matrix = for _i <- 0..6, do: for _j <- 0..6, do: @floors 
    map=gen_variants(init_map())
    {matrix,stat}= Enum.reduce_while(1..10, {matrix,0}, fn _step, {matr,prev_status} ->
      matr=matr|>check_cell(clues,map)|>additional_check_cell()
      stat=status(matr)
      if prev_status != stat, do: {:cont,{matr,stat}}, else: {:halt,{matr,stat}}
    end)
    {matrix,stat}= Enum.reduce_while(1..10, {matrix,stat}, fn _step, {matr,prev_status} ->
      matr=matr|>check_cell2(clues)|>additional_check_cell()
      stat=status(matr)
      if prev_status != stat, do: {:cont,{matr,stat}}, else: {:halt,{matr,stat}}
    end)
    matrix=(if stat > 49, do: check_imit(matrix,clues), else: matrix) 
    Enum.reduce(matrix, [], fn row,matr-> matr++[List.flatten(row)] end)
  end

  defp check_imit(matrix,clues) do
    arr=init_model(matrix)
    Enum.reduce(arr,matrix, fn {r,c}, matr1 ->
      arr=Enum.at(matr1,r)|>Enum.at(c)
      Enum.reduce_while(arr, matr1, fn el, matr ->
        matr_temp=set_value(matr,r,c,el)
        {matr_temp,stat}= Enum.reduce_while(1..10, {matr_temp,0}, fn _step, {matr,prev_status} ->
          matr=matr|>check_cell2(clues)|>additional_check_cell()
          stat=status(matr)
          if prev_status != stat, do: {:cont,{matr,stat}}, else: {:halt,{matr,stat}}
        end)
        if stat < 49 do 
          {:cont,matr} 
        else if stat == 49, do:  {:halt,matr_temp}, else: {:cont,matr_temp}
        end
      end)
    end)
  end

  defp init_model(matrix) do
    Enum.reduce(0..6,[], fn r, arr -> 
      Enum.reduce(0..6, arr, fn c, a -> if length(Enum.at(matrix,r)|>Enum.at(c)) > 1, do: a++[{r,c}], else: a end)
    end)
  end

  defp status(matrix) do
     Enum.reduce(0..6,0, fn j, sum1 -> Enum.reduce(0..6,sum1, fn i, sum -> sum+length(Enum.at(matrix,j)|>Enum.at(i)) end) end)
  end

  defp check_cell2(matrix,clues) do
    Enum.reduce(0..3, matrix, fn step,matr -> 
      clues1=Enum.slice(clues,step*7..((step+1)*7-1))
      matr=Enum.reduce(0..6, matr, fn col, m -> 
        clue=Enum.at(clues1,col)
        if clue != 0 do
          map2 = init_map2(matr,col)
          arr=gen_variants2(map2,clue)
          m|>act_on_col(clue,col,arr)|>check_uniq(col)|>check_duplicates(col)
        else
          m
        end
      end)  
      matr|>rotate
    end)
  end

  defp check_cell(matrix,clues,map) do
    Enum.reduce(0..3, matrix, fn step,matr -> 
      clues1=Enum.slice(clues,step*7..((step+1)*7-1))
      matr=Enum.reduce(0..6, matr, fn col, m -> 
        clue=Enum.at(clues1,col)
        m|>act_on_col(clue,col,map[clue])|>check_uniq(col)|>check_duplicates(col)
      end)  
      matr|>rotate
    end)
  end

  defp additional_check_cell(matrix) do
    Enum.reduce(0..3, matrix, fn _step,matr -> 
         matr=Enum.reduce(0..6, matr, fn col, m -> 
         m|>check_uniq(col)|>check_duplicates(col)
      end)  
      matr|>rotate
    end)
  end

  defp act_on_col(matrix,clue_top,col,variants) when clue_top > 0 and clue_top <= 7, do: set_column(matrix,col, variants)
  defp act_on_col(matrix,_clue_top,_col,_variants), do: matrix
  defp check_duplicates(matrix,col) do
    Enum.reduce(1..7, matrix, fn val,m -> 
       row = get_row_for(m,col,val) 
       if row >= 0, do: m|>del_values(@all--[row],[col],val)|>del_values([row],@all--[col],val), else: m 
     end)
  end

  defp check_uniq(matrix,col) do
     Enum.reduce(1..7, matrix, fn val,m -> 
      {num_val,row} = Enum.reduce(0..6, {0,0}, fn row, {num,r} -> 
        a=Enum.at(m,row)|>Enum.at(col)
        if Enum.member?(a,val), do: {num+1,row}, else: {num,r}
      end)
      if num_val == 1, do: set_value(m,row,col,val), else: m 
    end)
  end

  defp get_row_for(matrix, col, val) do
    Enum.reduce_while(0..6, -1, fn row, _ind -> 
        a=Enum.at(matrix,row)|>Enum.at(col)
        if length(a) == 1 && Enum.at(a,0) == val, do: {:halt,row}, else: {:cont,-1} 
      end)
  end

  defp del_value(matrix,row,col,value) do
    r=Enum.at(matrix,row)
    r=List.replace_at(r,col,Enum.at(r,col)--[value])
    List.replace_at(matrix,row,r)
  end
  defp del_values(matrix,rows,cols,value) do
    Enum.reduce(rows, matrix, fn row, matr1 -> 
      Enum.reduce(cols, matr1, fn col, matr2 -> del_value(matr2,row,col,value) end )
    end)
  end
  defp set_column(matrix,col, arr) do
     m=Enum.reduce( 0..6, matrix, fn row, matr ->
      r=Enum.at(matr,row)
      c=Enum.at(r,col)
      if length(c)>length(Enum.at(arr,row)) do 
        r=List.replace_at(r,col,intersect(c,Enum.at(arr,row)))
        List.replace_at(matr,row,r)
      else matr
      end
     end)
     m
  end
  defp intersect(a1,a2) do
     Enum.reduce( a1, [], fn el,arr->
        if Enum.member?(a2,el), do: arr++[el], else: arr
     end) 
  end
  defp set_value(matrix,row,col,value) do
    r=Enum.at(matrix,row)|>List.replace_at(col,[value])
    List.replace_at(matrix,row,r)
  end
  defp init_map2(m,col) do
    Enum.at(m,0)|>Enum.at(col)
    for a<-Enum.at(m,0)|>Enum.at(col),b<-Enum.at(m,1)|>Enum.at(col),c<-Enum.at(m,2)|>Enum.at(col),d<-Enum.at(m,3)|>Enum.at(col),
        e<-Enum.at(m,4)|>Enum.at(col),f<-Enum.at(m,5)|>Enum.at(col),j<-Enum.at(m,6)|>Enum.at(col),
        a not in [b,c,d,e,f,j], b not in [c,d,e,f,j], c not in [d,e,f,j], d not in [e,f,j], e not in [f,j], f != j,  do: [a,b,c,d,e,f,j]
  end  
  defp gen_variants2(map,clue) do
    Enum.reduce(map,[], fn el, m -> if get_vis(el) ==clue, do: m++[el], else: m end)|> merge
  end
  
  defp init_map do
    for a <- 1..7, b <- 1..7, c <- 1..7, d <- 1..7, e <- 1..7, f <- 1..7, j <- 1..7, 
      a not in [b,c,d,e,f,j], b not in [c,d,e,f,j], c not in [d,e,f,j], d not in [e,f,j], e not in [f,j], f != j,  do: [a,b,c,d,e,f,j]
  end
  defp gen_variants(a) do
      map=Enum.reduce(a,%{1=>[],2=>[],3=>[],4=>[],5=>[],6=>[],7=>[]}, fn el, m -> 
        vis = get_vis(el) 
        {_old,m}=Map.get_and_update(m,vis, fn cur -> {cur, cur++[el]} end)
        m
      end)
      Enum.reduce(1..7,map, fn key,m -> 
        {_,m}=Map.get_and_update(m,key, fn arr -> {arr,merge(arr)} end) 
        m 
      end)
  end
  defp get_vis(arr) do
      {_,vis,_} = Enum.reduce(arr, {0,0,0}, fn el,{prev,vis,max} -> comp(el,prev,vis,max) end)
      vis
  end
  defp comp(el,prev,vis,max) when el <= prev or el < max , do: {el,vis,max}
  defp comp(el,prev,vis,max) when el > prev and el > max , do: {el,vis+1,el}
  defp merge(a_in) do
    Enum.reduce(a_in,[[],[],[],[],[],[],[]], fn el, arr -> 
        Enum.reduce(0..6, arr, fn ind, a ->
         List.replace_at(a,ind,Enum.at(a,ind)++[Enum.at(el,ind)]|>Enum.uniq|>Enum.sort) end  )
    end)
  end
  defp rotate(matrix), do: matrix |> Enum.zip |> Enum.map(fn t -> :erlang.tuple_to_list(t) end) |> Enum.reverse
end

_____________________________________________________________________________
defmodule Helper do
    def permute([]), do: [[]]
    def permute(ls), do: ls
        |> Enum.with_index
        |> Enum.flat_map(fn {x,i} -> ls
            |> List.delete_at(i)
            |> permute
            |> Enum.map(& [x|&1])
        end)

    def rev_tuple(t), do: t |> Tuple.to_list |> Enum.reverse |> List.to_tuple
end

defmodule PuzzleSolver do
    @size 7

    @row_per_vis 1..@size
        |> Enum.to_list
        |> Helper.permute
        |> Enum.reduce(Map.new(0..@size, & {&1,MapSet.new}), fn p,m ->
            {_,v} = Enum.reduce(p, {0,0}, fn h,(a = {m,c}) ->
                if m < h, do: {h,c+1}, else: a
            end)
            p = List.to_tuple(p)
            m |> Map.put(0,MapSet.put(m[0],p)) |> Map.put(v,MapSet.put(m[v],p))
        end)

    defp fit(rfs, cfs) do
        if not Enum.any?(rfs, &Enum.empty?/1) do
            if Enum.all?(rfs, fn [_] -> true; _ -> false end) do
                Enum.map(rfs, &hd/1)
            else
                prev = rfs
                {rfs,cfs} = Enum.reduce(0..@size-1, {rfs,cfs}, fn i,a ->
                    Enum.reduce(0..@size-1, a, fn j,{r,c} ->
                        xs = Enum.at(c,i)
                        ys = Enum.at(r,j)
                        cmn = MapSet.intersection(
                            MapSet.new(xs, & elem(&1,j)),
                            MapSet.new(ys, & elem(&1,i))
                        )
                        {
                            List.replace_at(r, j, Enum.filter(ys, & elem(&1,i) in cmn)),
                            List.replace_at(c, i, Enum.filter(xs, & elem(&1,j) in cmn))
                        }
                    end)
                end)
                if prev == rfs, do: search(rfs,cfs), else: fit(rfs,cfs)
            end
        end
    end

    defp search(rfs, cfs) do
        {x,i} = rfs
            |> Enum.with_index
            |> Enum.reject(fn {[_],_} -> true; _ -> false end)
            |> Enum.min_by(fn {x,_} -> length(x) end)

        Enum.reduce(x, nil, fn p,r -> r || rfs |> List.replace_at(i,[p]) |> fit(cfs) end)
    end

    def solve(clues) do
        clues = List.to_tuple(clues)

        cfs = Enum.map(0..@size-1, fn i ->
            opc = elem(clues, 3*@size-i-1)
            MapSet.intersection(
                @row_per_vis[elem(clues,i)],
                MapSet.new(@row_per_vis[opc], &Helper.rev_tuple/1)
            ) |> MapSet.to_list
        end)

        rfs = Enum.map(@size..2*@size-1, fn i ->
            opc = elem(clues, 5*@size-i-1)
            MapSet.intersection(
                MapSet.new(@row_per_vis[elem(clues,i)], &Helper.rev_tuple/1),
                @row_per_vis[opc]
            ) |> MapSet.to_list
        end)

        rfs |> fit(cfs) |> Enum.map(&Tuple.to_list/1)
    end
end
