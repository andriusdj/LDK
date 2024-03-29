<?php

namespace App\Entity;

use App\Entity\ChestRecord;
use App\Entity\User;
use App\Repository\PlayerRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass=PlayerRepository::class)
 */
class Player
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255, unique=true)
     */
    private $name;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private $realName;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private $phone;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private $email;

    /**
     * @ORM\Column(type="integer", nullable=true)
     */
    private $level;

    /**
     * @ORM\OneToMany(targetEntity=ChestRecord::class, mappedBy="player")
     */
    private $chestRecords;

    /**
     * @ORM\ManyToOne(targetEntity=User::class, inversedBy="players")
     */
    private $user;


    public function __construct()
    {
        $this->chestRecords = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getRealName(): ?string
    {
        return $this->realName;
    }

    public function setRealName(?string $realName): self
    {
        $this->realName = $realName;

        return $this;
    }

    public function getPhone(): ?string
    {
        return $this->phone;
    }

    public function setPhone(?string $phone): self
    {
        $this->phone = $phone;

        return $this;
    }

    public function getEmail(): ?string
    {
        return $this->email;
    }

    public function setEmail(?string $email): self
    {
        $this->email = $email;

        return $this;
    }

    public function getLevel(): ?int
    {
        return $this->level;
    }

    public function setLevel(?int $level): self
    {
        $this->level = $level;

        return $this;
    }

    /**
     * @return Collection<int, ChestRecord>
     */
    public function getChestRecords(): Collection
    {
        return $this->chestRecords;
    }

    public function addChestRecord(ChestRecord $chestRecord): self
    {
        if (!$this->chestRecords->contains($chestRecord)) {
            $this->chestRecords[] = $chestRecord;
            $chestRecord->setPlayer($this);
        }

        return $this;
    }

    public function removeChestRecord(ChestRecord $chestRecord): self
    {
        if ($this->chestRecords->removeElement($chestRecord)) {
            // set the owning side to null (unless already changed)
            if ($chestRecord->getPlayer() === $this) {
                $chestRecord->setPlayer(null);
            }
        }

        return $this;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): self
    {
        $this->user = $user;

        return $this;
    }

    public function __toString(): string
    {
        return $this->getName();
    }

}
