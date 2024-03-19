<?php

namespace App\Command;

use App\Entity\User;
use RuntimeException;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Style\SymfonyStyle;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

class MakeSuperuserCommand extends Command
{
    protected static $defaultName = 'make:superuser';
    protected static $defaultDescription = 'Make a new super admin user or make super admin existing user';

    private $em;
    private $passwordHasher;
    private $users;

    public function __construct(
        EntityManagerInterface $entityManager,
        UserPasswordHasherInterface $passwordHasher,
        UserRepository $users
    ) {
        $this->em = $entityManager;
        $this->passwordHasher = $passwordHasher;
        $this->users = $users;
        parent::__construct();
    }

    protected function configure(): void
    {
        // $this
        //     ->addArgument('username', InputArgument::OPTIONAL, 'Argument description')
        //     ->addOption('option1', null, InputOption::VALUE_NONE, 'Option description')
        // ;
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);

        $username = $io->ask('Username');

        $user = $this->users->findOneBy(['username' => $username]);

        if (null === $user) {
            $user = new User();
            $user->setUsername($username);

            $password = $io->ask('Password');

            $hashedPassword = $this->passwordHasher->hashPassword($user, $password);
            $user->setPassword($hashedPassword);
        }

        $user->setRoles(['ROLE_SUPER_ADMIN']);
        
        $this->em->persist($user);
        $this->em->flush();

        $io->success('User "'.$username.'" now has role "ROLE_SUPER_ADMIN"');

        return Command::SUCCESS;
    }
}
