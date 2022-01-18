class ExamException(Exception):
      pass

class Diff():
      def __init__(self, ratio=1):
            self.ratio = ratio
            
            if self.ratio == None:
                  raise ExamException('La ratio deve esserci')
            
            if not isinstance(self.ratio, int) and not isinstance(self.ratio, float):
                  raise ExamException ('La ratio deve essere int o float')

            
            if self.ratio <= 0:
                  raise ExamException('La ratio deve essere maggiore di 0 ')

                  

      def compute(self, lista):
            if not isinstance(lista, list):
                  raise ExamException('Accetiamo solo liste')
            if len(lista)<2:
                  raise ExamException('La lista deve contenere almeno due elementi')

            ans = []
            for i in range(len(lista)-1):
                  try:
                        ans.append((lista[i+1]-lista[i])/self.ratio)
                  except TypeError:
                        raise ExamException('La lista contiene elementi non interi')

            return ans

                  
            


##
##diff = Diff('t')
##result = diff.compute([2,4,8,16])
##print(result)
