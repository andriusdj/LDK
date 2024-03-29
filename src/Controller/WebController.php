<?php

namespace App\Controller;

use App\Entity\ChestRecord;
use App\Entity\ChestValue;
use App\Entity\Player;
use App\Form\ChestValuesType;
use DateTime;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class WebController extends AbstractController
{
    private const FORMAT_DAY = 'Ymd';
    private const FORMAT_WEEK = 'YW';


    /**
     * @var EntityManagerInterface
     */
    private $em;

    public function __construct(EntityManagerInterface $em)
    {
        $this->em = $em;
    }

    #[Route("/")]
    public function index(): Response
    {
        return $this->render('web/index.html.twig', [
        ]);
    }

    #[Route("/scores")]
    public function scores(): Response
    {
        $players = $this->em->getRepository(Player::class)->findAll();
        $scores = [];
        foreach ($players as $player) {
            $scores[] = [
                'player' => $player->getName(),
                'day_score' => $this->getScoreByFormat($player->getName(), (new DateTime())->format(self::FORMAT_DAY), self::FORMAT_DAY),
                'week_score' => $this->getScoreByFormat($player->getName(), (new DateTime())->format(self::FORMAT_WEEK), self::FORMAT_WEEK),
            ];
        }

        return $this->render('web/scores.html.twig', [
            'scores' => $scores
        ]);
    }

    private function getScoreByFormat($name, $by, $format): int
    {
        $repo = $this->em->getRepository(Player::class);
        /**
         * @var Player
         */
        $player = $repo->findOneBy(['name' => $name]);

        /**
         * @var ChestRecord[]
         */
        $chests = $player->getChestRecords();
        $result = 0;
        foreach ($chests as $chest) {
            $collected = $chest->getCreated();
            if ($collected->format($format) === $by) {
                $result += $this->getChestValue($chest->getChestName(), $chest->getChestType());
            }
        }

        return $result;
    }

    private function getChestValue($chestName, $chestType): int
    {
        $repo = $this->em->getRepository(ChestValue::class);
        $chestValue = $repo->findOneBy(['name' => $chestName, 'type' => $chestType]);

        return $chestValue->value ?? 0;
    }

    #[Route("/values")]
    public function values(Request $request): Response
    {
        $chestValue = new ChestValue;
        $form = $this->createForm(ChestValuesType::class, $chestValue);

        if ($form->isValid() && $form->isSubmitted($request)) {
            // save
        }

        return $this->render('', ['form' => $form]);
    }
}
