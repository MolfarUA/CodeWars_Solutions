Module Kata
    Function Doubleton(ByVal num As Integer) As Integer
       dim testnumber as integer = num + 1
       do
            dim sumString as string =""
            for each letter in testnumber.tostring
                if not sumString.contains (letter) then
                    sumstring &=letter
                end if                
            next
            if sumString.count=2 then return testnumber
            testnumber +=1
       loop
        
    End Function
End Module

#################
Module Kata
    Function Doubleton(ByVal num As Integer) As Integer
        while true 
            num += 1
            if num.tostring().distinct().toArray().count = 2 then exit while
        end while
        return num
    End Function
End Module

##############
Module Kata
    Function Doubleton(ByVal num As Integer) As Integer
        dim ReturnValue as integer = num
        while true 
            ReturnValue += 1
            Dim CharEnum As System.Globalization.TextElementEnumerator = System.Globalization.StringInfo.GetTextElementEnumerator(ReturnValue)
            dim Numbers as new list(of integer) 
            while CharEnum.MoveNext()
                Numbers.add(CharEnum.Current)
            end while
            if Numbers.distinct().count =2 then exit while
        end while
        return ReturnValue
    End Function
End Module

################
Module Kata
    Function Doubleton(ByVal num As Integer) As Integer
        Dim s As String
        For i = num + 1 To 1000000
            s = i
            Dim uc = s.Distinct().ToArray()
            If uc.Count = 2 Then
                Return i
                Exit For
            End If
        Next
        Return -1
    End Function
End Module

###############
Imports System.Collections.Generic

Module Kata
    Const MAX_INPUT_FROM_PROBLEM_DESCRIPTION = 1000000
    Const MAX_RESULT_GIVEN_MAX_INPUT = 1000001
    
    Function Doubleton(ByVal num As Integer) As Integer
        If num > MAX_INPUT_FROM_PROBLEM_DESCRIPTION Then
            Throw New ArgumentException($"Input num {num} was greater than the maximum value that the problem description stated it would be! ({MAX_INPUT_FROM_PROBLEM_DESCRIPTION})")
        End If
        
        For n As Integer = num + 1 To MAX_RESULT_GIVEN_MAX_INPUT
            If IsDoubleton(n) Then
                Return n
            End If
        Next
    
        Throw New NotImplementedException("Logic path not considered")
    End Function
    
    Function IsDoubleton(ByVal num As Integer) As Boolean
        Dim allNumberCharacters = num.ToString().ToCharArray()
        Dim distinctNumberCharacters = New HashSet(Of Char)(allNumberCharacters)
        Return distinctNumberCharacters.Count = 2
    End Function
End Module
