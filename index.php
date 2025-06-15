<?php
// página php que recebe uma solicitação POST contendo o log criptografado e posta no bd

// verifica se a req é POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // recebe os dados json
    $data = file_get_contents('php://input');
    $json = json_decode($data, true);

    // verifica os campos necessários
    if (isset($json['uuid']) && isset($json['datahora']) && isset($json['log'])) {
        $uuid = $json['uuid'];
        $datahora = $json['datahora'];
        $log = $json['log'];

        // valida uuid
        if (!preg_match('/^[a-f0-9\-]{36}$/i', $uuid)) {
            echo json_encode(['status' => 'error', 'message' => 'UUID inválido.']);
            exit;
        }

        // valida datahora
        if(preg_match('/^\d{8}_\d{6}$/', $datahora)) {
            // extrai os dados
            $ano = substr($datahora, 0, 4);
            $mes = substr($datahora, 4, 2);
            $dia = substr($datahora, 6, 2);
            $hora = substr($datahora, 9, 2);
            $minuto = substr($datahora, 11, 2);
            $segundo = substr($datahora, 13, 2);

            // validação de data
            if (!checkdate($mes, $dia, $ano)) {
                echo json_encode(['status' => 'error', 'message' => 'Data inválida.']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
                exit;
            }

            // validação de hora
            if ($hora < 0 || $hora > 23 || $minuto < 0 || $minuto > 59 || $segundo < 0 || $segundo > 59) {
                echo json_encode(['status' => 'error', 'message' => 'Hora inválida.']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
                exit;
            }
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Formato de datahora inválido.']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
            exit;
        }

        // verifica se o log começa com '-----BEGIN PGP MESSAGE-----'
        if (strpos($log, '-----BEGIN PGP MESSAGE-----') === 0) {
            // remove qualquer coisa após '-----END PGP MESSAGE-----'
            $log = preg_replace('/-----END PGP MESSAGE-----.*/s', '-----END PGP MESSAGE-----', $log);

            // tenta conexão ao bd
            try {
                $host = getenv('DB_HOST_KL');
                $user = getenv('DB_USER_KL');
                $pass = getenv('DB_PASS_KL');
                $dbname = getenv('DB_NAME_KL');

                // conecta ao bd
                $conn = new mysqli($host, $user, $pass, $dbname);
                
                // verifica a conexão
                if ($conn->connect_error) {
                    throw new Exception('Conexão falhou: ' . $conn->connect_error);
                }
                
                // define o charset da conexão
                if (!$conn->set_charset("utf8mb4")) {
                    throw new Exception('Erro ao definir o charset: ' . $conn->error);
                }

                // executa a inserção
                $stmt = $conn->prepare('INSERT INTO logs (uuid, datahora, log) VALUES (?, ?, ?)');
                $stmt->bind_param('sss', $uuid, $datahora, $log);
                
                if ($stmt->execute()) {
                    echo json_encode(['status' => 'success', 'message' => 'Log inserido com sucesso.']);
                } else {
                    echo json_encode(['status' => 'error', 'message' => 'Erro de processamento (1213).']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
                }

                // encerra a conexão
                $stmt->close();
                $conn->close();
            } catch (Exception $e) {
                echo json_encode(['status' => 'error', 'message' => 'Erro de processamento (4104).']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
            }
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Erro de processamento (530).']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
        }
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Erro de processamento (609).']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Erro de processamento (42).']), '<br><br>what are you looking for? weirdo (ಠ_ಠ)';
}
?>
