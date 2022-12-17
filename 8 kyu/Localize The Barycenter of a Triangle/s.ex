5601c5f6ba804403c7000004


defmodule Barycenter do
  import Float, only: [round: 2]
  
  def bar_triang({x1,y1}, {x2,y2}, {x3,y3}) do
    {(x1 + x2 + x3) / 3 |> round(4), (y1 + y2 + y3) / 3 |> round(4)}
  end
end
__________________________________
defmodule Barycenter do
  def bar_triang({x1,y1}, {x2,y2}, {x3,y3}) do
    [x1 + x2 + x3, y1 + y2 + y3]
    |> Enum.map(&(&1 / 3))
    |> Enum.map(&Float.round(&1, 4))
    |> List.to_tuple()
  end
end
__________________________________
defmodule Barycenter do
  def bar_triang({x1,y1}, {x2,y2}, {x3,y3}) do
    {Float.round((x1 + x2 + x3) / 3, 4), Float.round((y1 + y2 + y3) / 3, 4)}
  end
end
__________________________________
defmodule Barycenter do
  def bar_triang({x1,y1}, {x2,y2}, {x3,y3}) do
    bc_x = Float.round((x1 + x2 + x3) / 3, 4)
    bc_y = Float.round((y1 + y2 + y3) / 3, 4)
    {bc_x, bc_y}
  end
end
