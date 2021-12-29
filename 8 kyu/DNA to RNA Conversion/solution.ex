defmodule Convertor do
  def dna_to_rna(dna), do: String.replace(dna, "T", "U")
end

_____________________________
defmodule Convertor do
  def dna_to_rna(dna) do
    String.replace dna, ~r/T/, "U"
  end
end

_____________________________
defmodule Convertor do
  @doc """
  Converts a strand of DNA to a strand of RNA.
  """
  @spec dna_to_rna(String.t()) :: String.t()
  def dna_to_rna(dna) do
    dna
    |> String.codepoints()
    |> Enum.map_join(&rna/1)
  end
  
  defp rna("G"), do: "G"
  defp rna("C"), do: "C"
  defp rna("A"), do: "A"
  defp rna("T"), do: "U"
end

_____________________________
defmodule Convertor do
  def dna_to_rna(dna) do
    Regex.replace(~r/T/, dna, "U", global: true)
  end
end

_____________________________
defmodule Convertor do
  def dna_to_rna(dna) do
    # TODO: ...
    String.replace(dna, "T", "U")
  end
end
