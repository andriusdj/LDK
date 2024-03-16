<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class WebController extends AbstractController
{
    /**
     * @Route("/", name="app_web")
     */
    public function index(): Response
    {
        return $this->render('web/index.html.twig', [
            'controller_name' => 'WebController',
        ]);
    }

    /**
     * @Route("/scores", name="app_web_scores")
     */
    public function scores(): Response
    {
        return $this->render('', [
            'controller_name' => 'WebController',
        ]);
    }
}
