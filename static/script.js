console.log("Script loaded successfully");

function displayResults(selectedUtxos, elementId, algorithmName, changeUtxo, append = false) {
    const resultsContainer = document.getElementById(elementId);

    // Display selected UTXOs
    selectedUtxos.forEach(utxo => {
        const coin = document.createElement('div');
        coin.classList.add('coin');
        coin.textContent = `${utxo.value} BTC`; // Assuming utxo.value is a number
        resultsContainer.appendChild(coin);
    });

    // Display change UTXO, if there is any
    if (changeUtxo && changeUtxo.value > 0) {
        const changeCoin = document.createElement('div');
        changeCoin.classList.add('coin', 'change');
        changeCoin.textContent = `${changeUtxo.value} BTC`;
        resultsContainer.appendChild(changeCoin);
    }
}


function displayFee(elementId, fee) {
    const resultsContainer = document.getElementById(elementId);
    if (!resultsContainer) {
        console.error(`Element with ID ${elementId} not found.`);
        return;
    }

    // Create a paragraph or any suitable element for displaying the fee
    const feeInfo = document.createElement('p');
    feeInfo.textContent = `Transaction Fee: ${fee} satoshis`;
    feeInfo.classList.add('transaction-fee'); // Optionally add a class for styling

    // Append the fee information to the results container
    resultsContainer.appendChild(feeInfo);
}

function formatFee(feeInSatoshis) {
    const feeInBTC = feeInSatoshis / 100000000; // Convert satoshis to BTC
    return `${feeInSatoshis} satoshis (${feeInBTC.toFixed(8)} BTC)`;
}

document.querySelectorAll('#navigation a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

let globalUTXOs = [];
let globalSelectedUTXOsCoinxpert = [];
let globalChangeCoinxpert = [];

document.addEventListener('DOMContentLoaded', (event) => {
    // Highlight sender column
    document.getElementById('utxo-form').classList.add('highlighted-border');

    // Event listener for UTXO form submission
    document.getElementById('utxo-form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission behavior
        // Clear previous UTXOs
        const wallet = document.getElementById('wallet');
        wallet.innerHTML = '';

        // Get UTXO values from the form
        const utxosInput = document.getElementById('utxo-input').value.split(',');
        globalUTXOs = utxosInput.map(value => parseFloat(value.trim())).filter(value => !isNaN(value));
        console.log(`Wallet UTXOs: ${globalUTXOs}`);

        // Validate and process each UTXO value
        globalUTXOs.forEach(value => {
            const coin = document.createElement('div');
            coin.classList.add('coin');
            coin.textContent = `${value} BTC`;
            wallet.appendChild(coin);
        });

        // Update highlights
        document.querySelector('.highlighted-border').classList.remove('highlighted-border');
        document.getElementById('target-form').classList.add('highlighted-border');

    });

    // Event listener for target form submission
    document.getElementById('target-form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Remove blur from algorith-column
        document.getElementById('algorithm-column').style.filter = 'none';
        document.getElementById('algorithm-column').style.pointerEvents = 'auto';
        document.getElementById('algorithm-column').style.userSelect = 'auto';

        // Get target amount from the form
        const targetAmount = parseFloat(document.getElementById('target-amount').value);
        console.log(`Target amount: ${targetAmount} BTC`);

         // Disables the button
        const submitBtn = document.getElementById('submit-target-amount-btn');
        submitBtn.disabled = true;

        try {
            const response = await fetch('/select_utxos/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({utxos: globalUTXOs.map(value => ({value})), target: targetAmount}),
            });

            if (!response.ok) {
                const errorData = await response.json();
                const errorMessageElement = document.getElementById('error-message');
                errorMessageElement.textContent = `${errorData.detail}`;
                errorMessageElement.style.display = 'block';
                // Immediately display the "Start New Transaction" button upon error
                document.getElementById('reset-transaction-btn').style.display = 'inline-block';

                // Optionally, remove or adjust any UI elements that are not needed due to the error
                document.getElementById('algorithm-column').style.filter = 'blur(200px)'; // Hide the algorithm column

                // Update highlights to focus on the error or reset button
                document.querySelector('.highlighted-border').classList.remove('highlighted-border');

                 // After processing is complete, show the reset button
                document.getElementById('reset-transaction-btn-container-error-amount').style.display = 'flex';
                document.getElementById('reset-transaction-btn-error-amount').style.display = 'flex';
                document.getElementById('reset-transaction-btn-error-amount').addEventListener('click', function() {
                    window.location.reload();
                });

                return;
            }

            const {
                selected_utxos_core,
                change_utxo_core,
                selected_utxos_coinxpert,
                change_utxo_coinxpert,
                fee_btc_core,
                fee_coinxpert
            } = await response.json();

            globalSelectedUTXOsCoinxpert = selected_utxos_coinxpert
            globalChangeCoinxpert = change_utxo_coinxpert

            document.getElementById('bitcoin-core-fee-value').textContent = formatFee(fee_btc_core);
            document.getElementById('coinxpert-fee-value').textContent = formatFee(fee_coinxpert);
            displayResults(selected_utxos_core, 'bitcoin-core-results', 'Bitcoin Core', change_utxo_core);
//            displayResults(selected_utxos_greedy, 'coinxpert-results-greedy', 'CoinXpert (Greedy)', change_utxo_greedy);
            displayResults(selected_utxos_coinxpert, 'coinxpert-results', 'CoinXpert', change_utxo_coinxpert);

        } catch (error) {
            console.error('Failed to fetch algorithm results:', error);
            // Display error message for network errors or other issues
            const errorMessageElement = document.getElementById('error-message');
            errorMessageElement.textContent = 'Failed to process the transaction. Please try again.';
            errorMessageElement.style.display = 'block';
        }

        document.getElementById('process-transaction-btn').style.display = 'inline-block';

        // Update highlights
        document.querySelector('.highlighted-border').classList.remove('highlighted-border');
        document.getElementById('process-transaction-btn-container').classList.add('highlighted-border');
    });

    document.getElementById('process-transaction-btn').addEventListener('click', async function(event) {

        // Remove blur from algorith-column
        document.getElementById('receiver-column').style.filter = 'none';
        document.getElementById('receiver-column').style.pointerEvents = 'auto';
        document.getElementById('receiver-column').style.userSelect = 'auto';

        // Update highlights
        document.querySelector('.highlighted-border').classList.remove('highlighted-border');

        // Ensure global variables or DOM elements store the necessary CoinXpert results and target amount
        const targetAmountElement = document.getElementById('target-amount');
        const targetAmount = parseFloat(targetAmountElement.value);

        // Update the receiver wallet
        const receiverWallet = document.getElementById('wallet_receive');
        const transactionCoin = document.createElement('div');
        transactionCoin.classList.add('coin');
        transactionCoin.textContent = `${targetAmount} BTC`; // Display target amount as a coin
        receiverWallet.appendChild(transactionCoin);

        // CoinXpert results might have been stored globally or need to be fetched from the DOM
        const selectedUtxos = globalSelectedUTXOsCoinxpert || []; // This should be set when displaying results
        const changeUtxo = globalChangeCoinxpert || {}; // Assuming these are set when displaying CoinXpert results

        // Update the sender wallet: remove used UTXOs and add change if necessary
        const senderWallet = document.getElementById('wallet');
        senderWallet.innerHTML = ''; // Clear and rebuild sender wallet

        const globalUTXOsFormatted = globalUTXOs.map(val => ({ value: val }));
        const remainingUTXOs = globalUTXOsFormatted.filter(utxoGlobal =>
        !globalSelectedUTXOsCoinxpert.some(utxoSelected => utxoSelected.value === utxoGlobal.value));

        remainingUTXOs.forEach(utxo => {
            // Re-add coins that weren't used in the transaction
            const coin = document.createElement('div');
            coin.classList.add('coin');
            coin.textContent = `${utxo.value} BTC`;
            senderWallet.appendChild(coin);
        });

        if (changeUtxo.value > 0) {
            // Add the change UTXO as a gray coin
            const changeCoin = document.createElement('div');
            changeCoin.classList.add('change');
            changeCoin.textContent = `${changeUtxo.value} BTC`;
            senderWallet.appendChild(changeCoin);
        }

        // After processing is complete, show the reset button
        document.getElementById('reset-transaction-btn-container').style.display = 'flex';
        document.getElementById('reset-transaction-btn').style.display = 'flex';
    });

    document.getElementById('reset-transaction-btn').addEventListener('click', function() {window.location.reload();
    });
});