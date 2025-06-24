function atualizarEndereco() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    const numero = document.getElementById('numero').value;
    const complemento = document.getElementById('complemento').value;

    if (cep.length !== 8) {
        // Limpa os campos se CEP inválido
        document.getElementById('rua').value = '';
        document.getElementById('bairro').value = '';
        document.getElementById('cidade').value = '';
        document.getElementById('estado').value = '';
        document.getElementById('endereco').value = '';
        return;
    }

    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(res => res.json())
        .then(data => {
            if (data.erro) {
                alert("CEP não encontrado.");
                document.getElementById('rua').value = '';
                document.getElementById('bairro').value = '';
                document.getElementById('cidade').value = '';
                document.getElementById('estado').value = '';
                document.getElementById('endereco').value = '';
                return;
            }

            document.getElementById('rua').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
            document.getElementById('estado').value = data.uf || '';

            let enderecoCompleto = `${data.logradouro || ''}, ${numero}`;
            if (complemento) {
                enderecoCompleto += ` - ${complemento}`;
            }
            enderecoCompleto += ` - ${data.bairro || ''}, ${data.localidade || ''} - ${data.uf || ''}`;

            document.getElementById('endereco').value = enderecoCompleto;
        })
        .catch(() => {
            alert("Erro ao consultar o CEP.");
        });
}

document.getElementById('cep').addEventListener('blur', atualizarEndereco);
['numero', 'complemento'].forEach(id => {
    document.getElementById(id).addEventListener('input', atualizarEndereco);
});
