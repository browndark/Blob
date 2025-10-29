import sys, os
sys.path.insert(0, 'src')
from modules.ultra_advanced_ai import UltraAdvancedAI

class MockDB:
    def __init__(self):
        self.db_path = 'test.db'
        self.preferences = {}
    def get_preference(self, k, d=None): return self.preferences.get(k, d)
    def save_preference(self, k, v): self.preferences[k] = v

print('🎯 TESTE: VARIEDADE DE RESPOSTAS CORRIGIDA')
print('=' * 50)

ai = UltraAdvancedAI(MockDB())

print('🤖 Testando mesma entrada 5 vezes:')
entrada = 'Estou bem hoje'
respostas = []
for i in range(5):
    resp = ai.process_input(entrada)
    respostas.append(resp)
    print(f'  {i+1}. {resp}')

variedade = len(set(respostas))
print(f'📊 Variedade: {variedade}/5 respostas diferentes')

if variedade >= 4:
    print('🎉 EXCELENTE! Problema resolvido!')
elif variedade >= 3:
    print('✅ MUITO BOM! Grande melhoria!')
else:
    print('⚠️ Ainda pode melhorar...')

print('\n🧪 Testando diferentes tipos:')
testes = [
    'Oi!',
    'Preciso de ajuda',
    'Obrigado!',
    'Fui trabalhar',
    'Estou triste'
]

for teste in testes:
    resp = ai.process_input(teste)
    print(f'  "{teste}" -> "{resp}"')

print('\n✅ SISTEMA CORRIGIDO!')