<?php

namespace App\Entity;

use App\Entity\Player;
use App\Repository\ChestRecordRepository;
use DateTime;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass=ChestRecordRepository::class)
 */
class ChestRecord
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;


    /**
     * @ORM\Column(type="string", length=255)
     */
    private $chestName;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $chestType;

    /**
     * @ORM\Column(type="datetime")
     */
    private $created;

    /**
     * @ORM\Column(type="datetime")
     */
    private $recorded;

    /**
     * @ORM\ManyToOne(targetEntity=Player::class, inversedBy="chestRecords")
     * @ORM\JoinColumn(nullable=false)
     */
    private $player;


    public function getId(): ?int
    {
        return $this->id;
    }

    public function getChestName(): ?string
    {
        return $this->chestName;
    }

    public function setChestName(string $chestName): self
    {
        $this->chestName = $chestName;

        return $this;
    }

    public function getChestType(): ?string
    {
        return $this->chestType;
    }

    public function setChestType(string $chestType): self
    {
        $this->chestType = $chestType;

        return $this;
    }

    public function getCreated(): ?\DateTimeInterface
    {
        return $this->created;
    }

    public function setCreated(\DateTimeInterface $created): self
    {
        $this->created = $created;

        return $this;
    }

    public function getRecorded(): ?\DateTimeInterface
    {
        return $this->recorded;
    }

    public function setRecorded(\DateTimeInterface $recorded): self
    {
        $this->recorded = $recorded;

        return $this;
    }

    public function getPlayer(): ?Player
    {
        return $this->player;
    }

    public function setPlayer(?Player $player): self
    {
        $this->player = $player;

        return $this;
    }

    public static function createFromRecord(array $record): self
    {
        $chestRecord = new self();
        $chestRecord->setChestName($record['chest_name']);
        $chestRecord->setChestType($record['chest_type']);
        /**
         * DateTime
         */
        $recorded = DateTime::createFromFormat('U.u', $record['recorded']);
        $chestRecord->setRecorded($recorded);

        $hour = 0;
        $minute = 0;
        $second = 0;

        $expiration = $record['expiring_in'];
        if (count($expiration) > 1) {
            $hour = trim($expiration[0], "h");
            $minute = trim($expiration[1], "m");
        } elseif (count($expiration) === 1 && strstr($expiration[0], "m")) {
            $minute = $expiration[0];
        } elseif (count($expiration) === 1 && strstr($expiration[0], "s")) {
            $second = $expiration[0];
        }

        $hour = 20 - self::numerizeOcr($hour);
        $minute = 60 - self::numerizeOcr($minute);
        $second = 60 - self::numerizeOcr($second);
        
        $created = clone $recorded;
        $created->modify("-$hour hours -$minute minutes -$second seconds");

        $chestRecord->setCreated($created);
        
        return $chestRecord;
    }

    private static function numerizeOcr($number): int
    {
        if (in_array($number, ['i', 'l', 'j', 'I'])) {
            $number = 1;
        }

        if (in_array($number, ['o', 'O', 'U', 'D'])) {
            $number = 0;
        }

        return (int) $number;
    }
}
