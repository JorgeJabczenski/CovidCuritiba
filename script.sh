# Arquivo de Saida
outFile="outFile"

# Baixa a pagina
wget -nv --no-hsts "https://coronavirus.curitiba.pr.gov.br"

# Declara Variaveis
declare -a infos=("lblSuspeitos" "lblConfirmados" "lblObitos"  "lblLeitosLivres" "lblOcupacao" "lblObitos")
declare -a vacina=("lblContadorVacinas" "lblContadorSegundaDose")

# Data Atualizacao
dataAtualizacao=$(cat index.html | grep 'lblDataAtualizacao' | tail -1 | cut -d'>' -f2 | cut -d'<' -f1)
echo $dataAtualizacao > $outFile

# Situação Atual
for i in "${infos[@]}"
do
    echo "$i" >> $outFile
    cat index.html | grep "$i" | cut -d'>' -f2 | cut -d'<' -f1 >> $outFile
done

# Data Vacina
dataVacinacao=$(cat index.html | grep 'lblDataAtualizacaoVacinacao' | tail -1 | cut -d'>' -f2 | cut -d'<' -f1)
echo "Atualizacao da Vacina: $dataVacinacao" >> $outFile

# Vacinacao
for i in "${vacina[@]}"
do
    echo "$i" >> $outFile
    cat index.html | grep "$i" | cut -d'>' -f3 | cut -d '<' -f1 >> $outFile
done

# Bandeira Atual
bandeira=$(cat index.html | grep "evidencia" | cut -d'"' -f4 | cut -d' ' -f2) 

if [ "$bandeira" = "altoRisco" ]; then
    echo "Bandeira Vermelha" >> $outFile
elif [ "$bandeira" = "riscoModerado" ]; then
    echo "Bandeira Laranja" >> $outFile
else
    echo "Bandeira Amarela" >> $outFile
fi

# Chama o código para construir e postar o tweet
python3 covid.py

rm $outFile
rm index.html
