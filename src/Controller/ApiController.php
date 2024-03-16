<?php

namespace App\Controller;

use App\Entity\ChestRecord;
use App\Entity\Player;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class ApiController extends AbstractController
{
    /**
     * @Route("/api", name="app_api")
     */
    public function index(): Response
    {
        return $this->json(["status" => "error", "message" => "no access"]);
    }
    /**
    * @Route("/api/submit", name="app_api_submit")
    */
    public function submit(EntityManagerInterface $em, Request $request): Response
    {
    	$json = json_decode($request->getContent(), true);
    	$token = $json['token'] ?? null;
		$expectedToken = $this->getParameter("token");

    	if ($token !== $expectedToken) {

    		return $this->json(["status" => "error", "message" => "invalid token"], Response::HTTP_FORBIDDEN);
    	}

		try {
			/**
			 * @var App\Repository\PlayerRepository
			 */
			$playerRepo = $em->getRepository(Player::class);

			$data = $json['data'];
			foreach ($data as $record) {
				/**
				 * @var Player
				 */
				$player = $playerRepo->findOneBy(['name' => $record['player']]);
				if (!$player) {
					$player = new Player();
					$player->setName($record['player']);				
				}

				$chestRecord = ChestRecord::createFromRecord($record);
				$player->addChestRecord($chestRecord);
				
				$em->persist($player);
				$em->persist($chestRecord);
				$em->flush();

			}

			return $this->json(["status" => "OK", "data" => $data]);

		} catch (\Exception $e) {

			return $this->json(["status" => "ERROR", "message" => $e->getMessage()], Response::HTTP_INTERNAL_SERVER_ERROR);
		}
    }
}

