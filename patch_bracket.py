import re

file_path = "templates/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the HTML Bracket Section
new_bracket_html = """        <!-- Seção do Mata-Mata -->
        <div class="mt-16 mb-8 w-full overflow-x-auto pb-12">
            <h3 class="text-4xl font-bold text-center text-gray-800 mb-12">Mata-mata</h3>
            <div class="flex justify-center items-center min-w-[1600px] gap-6 px-8">
                
                <!-- Lado Esquerdo -->
                <div class="flex gap-8 w-1/2 justify-end">
                    <!-- R32 -->
                    <div class="flex flex-col justify-around gap-2 py-2">
                        {% for i in "1234567890123456"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-10 h-10 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="r32" data-index="{{ forloop.counter }}"></div>
                        {% endfor %}
                    </div>
                    <!-- R16 -->
                    <div class="flex flex-col justify-around gap-4 py-4">
                        {% for i in "12345678"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-14 h-14 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="r16" data-index="{{ forloop.counter }}"></div>
                        {% endfor %}
                    </div>
                    <!-- QF -->
                    <div class="flex flex-col justify-around gap-8 py-8">
                        {% for i in "1234"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-16 h-16 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="qf" data-index="{{ forloop.counter }}"></div>
                        {% endfor %}
                    </div>
                    <!-- SF -->
                    <div class="flex flex-col justify-around gap-16 py-16">
                        {% for i in "12"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-20 h-20 flex items-center justify-center bg-white shadow-md cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="sf" data-index="{{ forloop.counter }}"></div>
                        {% endfor %}
                    </div>
                </div>
                
                <!-- Centro (Final e Campeão) -->
                <div class="flex flex-col items-center justify-center px-8 gap-8">
                    <div class="text-center brand-text text-sm font-bold">Clique nas bandeiras<br>para avançar</div>
                    <div class="flex items-center gap-6">
                        <div class="bracket-node border-4 border-blue-400 rounded-full w-24 h-24 flex items-center justify-center bg-white shadow-lg cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="final" data-index="1"></div>
                        <div class="bracket-node border-4 border-yellow-400 rounded-full w-32 h-32 flex items-center justify-center bg-gray-50 shadow-inner overflow-hidden" data-round="champion" data-index="1">
                            <span class="text-5xl">🏆</span>
                        </div>
                        <div class="bracket-node border-4 border-blue-400 rounded-full w-24 h-24 flex items-center justify-center bg-white shadow-lg cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="final" data-index="2"></div>
                    </div>
                </div>
                
                <!-- Lado Direito -->
                <div class="flex gap-8 w-1/2 justify-start">
                    <!-- SF -->
                    <div class="flex flex-col justify-around gap-16 py-16">
                        {% for i in "34"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-20 h-20 flex items-center justify-center bg-white shadow-md cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="sf" data-index="{{ i }}"></div>
                        {% endfor %}
                    </div>
                    <!-- QF -->
                    <div class="flex flex-col justify-around gap-8 py-8">
                        {% for i in "5678"|make_list %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-16 h-16 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="qf" data-index="{{ i }}"></div>
                        {% endfor %}
                    </div>
                    <!-- R16 -->
                    <div class="flex flex-col justify-around gap-4 py-4">
                        {% for i in "9,10,11,12,13,14,15,16"|split:"," %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-14 h-14 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="r16" data-index="{{ i }}"></div>
                        {% endfor %}
                    </div>
                    <!-- R32 -->
                    <div class="flex flex-col justify-around gap-2 py-2">
                        {% for i in "17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32"|split:"," %}
                        <div class="bracket-node border-2 border-gray-300 rounded-full w-10 h-10 flex items-center justify-center bg-white shadow-sm cursor-pointer hover:bg-blue-50 transition overflow-hidden" data-round="r32" data-index="{{ i }}"></div>
                        {% endfor %}
                    </div>
                </div>
                
            </div>
        </div>"""

content = re.sub(r'<!-- Seção do Mata-Mata -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', new_bracket_html, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patch applied")
