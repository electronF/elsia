<?php

/*
|-------------------------------------------
| Welcome to Laravel Playground
|-------------------------------------------
|
| Laravel Playground allows you to try out PHP and Laravel all from your browser.
| You have access to all Laravel classes and an extensive list of included
| Laravel packages (like Laravel DebugBar).
|
| You can also load your own Gists! 
| Simply append /gist/{YOUR-GIST-ID} to the URL.
|
| Do you want to see some examples?
|
| Multiple views: https://laravelplayground.com/#/gist/d990a2c5f23b50564561b9266252f501
| Form request validation: https://laravelplayground.com/#/gist/e5a0d029f6433e31672e55dd90429d3f
| Livewire: https://laravelplayground.com/#/gist/286de510bfc0a88e697284e90ed1d7da
|
*/

// Route::get('/', function (){
//   return view('playground', [
//     'title' => 'Laravel Playground'
//   ]);
// });


use Illuminate\Support\Facades\Http;
$urlBase = 'https://aadc41f9ed08.ngrok-free.app/api/v1';
//As this a temporary url, it will change after some time. You can use your own ngrok link or deploy the FastAPI on a server. Or just use the localhost if you are running the FastAPI locally. 
// Or use the localhost if you are running the FastAPI locally (on AWS EC2 server where the app is located and then the link should look like http://localhost:8000/api/v1, the port can be differente).



// This code is write for php artisan tinker


echo 'Strengths';
//------------------------------------------------------
// This part is for Challenges
//------------------------------------------------------


$l = $urlBase.'/strengths/';

$data = [
    'age'         => 21.5,
    'description' => "He is good at mathematics and physics",
];

// Envoi JSON correct (Content-Type + encodage gérés automatiquement)
$response = Http::acceptJson()
    ->asJson()
    ->post($l, $data);

// Affichage résultat
if ($response->successful()) {
    dump('OK', $response->json());
} else {
    dump('Erreur', $response->status(), $response->body());
}

// This is another version
$url = $urlBase.'/challenges/';

$data = [
    'age' => 21.5,
    'description' => "He has trouble managing his time and feels stressed before exams."
];

$response = Http::withHeaders([
    'accept' => 'application/json',
    'Content-Type' => 'application/json',
])->post($url, $data);

// Vérification du succès
if ($response->successful()) {
    echo 'Réponse reçue avec succès : ' . $response->body();
} else {
    echo 'Erreur : ' . $response->status();
}

// --------------- END ------------------------






echo 'Challenges';
//------------------------------------------------------
// This part is for Challenges
//------------------------------------------------------


$l = $urlBase.'/challenges/';

$data = [
    'age'         => 21.5,
    'description' => "He has trouble managing his time and feels stressed before exams.",
];

// Envoi JSON correct (Content-Type + encodage gérés automatiquement)
$response = Http::acceptJson()
    ->asJson()
    ->post($l, $data);

// Affichage résultat
if ($response->successful()) {
    dump('OK', $response->json());
} else {
    dump('Erreur', $response->status(), $response->body());
}

//--------------- END ------------------------




echo 'Goals';
//------------------------------------------------------
// This part is for Goals
//------------------------------------------------------



$l = $urlBase.'/goals/';

$data = [
    'age'        => 21.5,
    'challenges' => [
        'Difficulty with time management',
        'Anxiety before exams',
    ],
    'gender'     => 'female',
    'needs'      => [],
    'strengths'  => [
        'Strong teamwork skills',
        'Excellent listening skills',
        'Creative problem-solving',
    ],
];

$response = \Illuminate\Support\Facades\Http::acceptJson()
    ->asJson()        // envoie Content-Type: application/json + encode le body
    ->timeout(30)
    ->post($l, $data);

// Affichage résultat
if ($response->successful()) {
    dump('OK', $response->json());
} else {
    dump('Erreur', $response->status(), $response->json('detail') ?? $response->body());
}

//--------------- END ------------------------


echo 'Means';
//------------------------------------------------------
// This part is for Means
//------------------------------------------------------

$l = $urlBase.'/means/';

$data = [
    'age'        => 21.5,
    'challenges' => [
        'Difficulty with time management',
    ],
    'gender'     => 'female',
    'goals'      => [
        'Develop a weekly study schedule',
    ],
    'needs'      => [
        'Personalized study plan',
    ],
    'strengths'  => [
        'Strong teamwork skills',
    ],
];

$response = \Illuminate\Support\Facades\Http::acceptJson()
    ->asJson()     // envoie Content-Type: application/json + encodage JSON
    ->timeout(30)
    ->post($l, $data);

if ($response->successful()) {
    dump('OK', $response->json());
} else {
    dump('Error', $response->status(), $response->json('detail') ?? $response->body());
}



//--------------- END ------------------------

echo 'Full profile';
//------------------------------------------------------
// This part is for full profile description information
//------------------------------------------------------

// $url = $urlBase.'/profile/full/';

// $res = \Illuminate\Support\Facades\Http::acceptJson()
//     // Champs texte -> multipart (comme -F de curl)
//     ->attach('description', 'Je decris le contenu de ce champ')
//     ->attach('age', '21')
//     ->attach('gender', 'female')

//     // FICHIER (décommente si tu veux l’envoyer)
//     // ->attach('file', fopen(base_path('photo.png'), 'r'), 'photo.png')

//     ->post($url);

// // Inspecte la réponse
// dump('STATUS', $res->status());
// dump('RESPONSES', $res->body());

// // Pour voir l'erreur précise FastAPI en 422
// dump('ERROR', $res->json('detail'));


$url = $urlBase.'/profile/full/';

$http = \Illuminate\Support\Facades\Http::acceptJson();#->timeout(120)

// Décommente la ligne ->attach('file', ...) pour envoyer un fichier local
$res = $http
    ->attach('description', 'Je decris le contenu de ce champ')
    ->attach('age', '21')        // FastAPI va caster
    ->attach('gender', 'female')
    // ->attach('file', fopen(base_path('photo.png'), 'r'), 'photo.png')
    ->post($url);

// Inspection rapide
dump($res->status(), $res->headers());
if ($res->successful()) {
    dump($res->json() ?? $res->body());
} else {
    // FastAPI 422 donne souvent des détails utiles ici
    dump('Erreur', $res->status(), $res->json('detail') ?? $res->body());
}



//--------------- END ------------------------



?>