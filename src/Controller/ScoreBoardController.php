<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class ScoreBoardController extends AbstractController
{
    /**
     * @Route("/score/board", name="app_score_board")
     */
    public function index(): Response
    {
        return $this->render('score_board/index.html.twig', [
            'controller_name' => 'ScoreBoardController',
        ]);
    }
}
