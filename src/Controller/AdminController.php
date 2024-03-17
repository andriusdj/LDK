<?php

namespace App\Controller;

use App\Entity\Player;
use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class AdminController extends AbstractController
{
    /**
     * @Route("/admin", name="app_admin")
     */
    public function index(): Response
    {
        return $this->render('admin/index.html.twig', [
        ]);
    }
    
    /**
     * @Route("/admin/users", name="app_admin_users")
     */
    public function users(EntityManagerInterface $em): Response
    {
        $users = $em->getRepository(User::class)->findAll();

        return $this->render('admin/index.html.twig', [
            'users' => $users,
        ]);
    }

    /**
     * @Route("/admin/players", name="app_admin_players")
     */
    public function players(EntityManagerInterface $em): Response
    {
        $players = $em->getRepository(Player::class)->findAll();

        return $this->render('admin/index.html.twig', [
            'players' => $players,
        ]);
    }
}
